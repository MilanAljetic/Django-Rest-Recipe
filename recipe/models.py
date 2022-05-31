from django.db import models
from django.db.models import Avg

from user.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    text = models.TextField()
    ingredient = models.ManyToManyField(Ingredient, related_name='ingredients')

    @property
    def calculate_average_rate(pk):
        return Rate.objects.filter(recipe=pk).aggregate(Avg("rate"))['rate__avg']

    def __str__(self):
        return self.name


RATE_CHOICES = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
]


class Rate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

    def __str__(self):
        return self.recipe.name
