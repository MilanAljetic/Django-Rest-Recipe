from django.db.models import Avg

from .models import Rate


def recipe_owner(data):
    recipe = data.get("recipe")
    if recipe.author == data.get("user"):
        return True
    return False


def check_if_user_rated_ones(data):
    if Rate.objects.filter(user=data.get("user"), recipe=data.get("recipe")).exists():
        return True
    return False


def average_rate(pk):
    return Rate.objects.filter(recipe=pk).aggregate(Avg("rate"))['rate__avg']
