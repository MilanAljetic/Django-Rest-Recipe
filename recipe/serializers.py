from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from user.models import User

from .models import Ingredient, Rate, Recipe
from .utils import average_rate, check_if_user_rated_ones, recipe_owner


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("first_name", "last_name")


class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ("name", )


class CreateRecipesSerializer(serializers.ModelSerializer):

    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Recipe
        fields = ("author", "name", "text", "ingredient")


class RecipesSerializer(serializers.ModelSerializer):
    calculate_average_rate = serializers.ReadOnlyField()
    ingredient = IngredientsSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ("author", "name", "text", "ingredient", "calculate_average_rate")

    def average_rate(self, obj):
        return average_rate(obj.pk)


class RatingSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Rate
        fields = ("user", "recipe", "rate")

    def create(self, validated_data):
        if recipe_owner(validated_data):
            raise ValidationError("Can't rate your recipe!")
        if check_if_user_rated_ones(validated_data):
            raise ValidationError("You already voted once!")
        return Rate.objects.create(**validated_data)
