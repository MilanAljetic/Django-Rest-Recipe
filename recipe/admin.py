from django.contrib import admin
from .models import Recipe, Ingredient, Rate


admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Rate)
