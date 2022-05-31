from django.contrib import admin
from django.urls import include, path

app_name = "user"

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/user/", include("user.urls")),
    path("api/", include("recipe.urls"))
]
