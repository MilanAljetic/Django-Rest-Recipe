from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from user.views import RegisterUserView, UserInfo

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name="user_register"),
    path('login/', TokenObtainPairView.as_view(), name='user_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('<int:pk>/', UserInfo.as_view(), name="user_info"),
]
