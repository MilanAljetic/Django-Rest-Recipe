from rest_framework import serializers

from user.models import User
from user.utils import clearbit_info, hunter_verify


class CreateAccountSerializer(serializers.ModelSerializer):

    password = serializers.CharField(style={"input_type": "password"}, required=True)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password",)

    def validate(self, attrs):
        if not hunter_verify(attrs['email']):
            raise serializers.ValidationError("Email is not valid")
        return attrs

    def create(self, validated_data):
        acc = User.objects.create(
            email=validated_data.get("email"),
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
        )
        acc.set_password(validated_data.get('password'))
        acc.save()
        return acc


class AccountSerializer(serializers.ModelSerializer):
    clear_bit = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "clear_bit")

    def get_clear_bit(self, obj):
        return clearbit_info(obj.email)
