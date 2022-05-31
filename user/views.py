from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated

from user.models import User
from user.serializers import AccountSerializer, CreateAccountSerializer


class RegisterUserView(generics.GenericAPIView, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = CreateAccountSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserInfo(generics.GenericAPIView, mixins.RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
