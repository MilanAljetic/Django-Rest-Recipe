from django.db.models import Count
from rest_framework import filters, generics, mixins
from rest_framework.permissions import IsAuthenticated

from .models import Ingredient, Rate, Recipe
from .serializers import (CreateRecipesSerializer, IngredientsSerializer,
                          RatingSerializer, RecipesSerializer)


class IngredientsView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CreateRecipesView(generics.GenericAPIView, mixins.CreateModelMixin):
    queryset = Recipe.objects.select_related("author").prefetch_related("ingredient").all()
    serializer_class = CreateRecipesSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class AllRecipesView(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Recipe.objects.prefetch_related("ingredient").all()
    serializer_class = RecipesSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name", "text", "ingredient__name",)

    def get_queryset(self):
        queryset = Recipe.objects.prefetch_related("ingredient").all()

        max_ingredient_num = self.request.query_params.get("max_ing_num", None)
        if max_ingredient_num:
            queryset = queryset.annotate(total=Count("ingredient")).filter(total__lte=int(max_ingredient_num))
        min_ingredient_num = self.request.query_params.get("min_ing_num", None)
        if min_ingredient_num:
            queryset = queryset.annotate(total=Count("ingredient")).filter(total__gte=int(min_ingredient_num))
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OwnRecipesView(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Recipe.objects.prefetch_related("ingredient").all()
    serializer_class = RecipesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Recipe.objects.filter(author=self.request.user.id)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RateView(generics.GenericAPIView, mixins.CreateModelMixin):
    queryset = Rate.objects.select_related("user").all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, requests, *args, **kwargs):
        return self.create(requests, *args, **kwargs)
