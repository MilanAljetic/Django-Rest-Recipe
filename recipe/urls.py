from django.urls import path

from .views import (AllRecipesView, CreateRecipesView, IngredientsView,
                    OwnRecipesView, RateView)

urlpatterns = [
    path("ingredients/", IngredientsView.as_view(), name="ingredients"),
    path("recipes/create/", CreateRecipesView.as_view(), name="create_recipes"),
    path("recipes/", AllRecipesView.as_view(), name="all_recipes"),
    path("recipes/user/", OwnRecipesView.as_view(), name="user_recipes"),
    path("recipes/rate/", RateView.as_view(), name="rate")
]
