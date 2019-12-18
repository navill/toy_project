from rest_auth.registration.views import RegisterView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from accounts.serializers import CustomUserDetailSerializer, CustomRegisterSerializer


class CustomRegisterView(RegisterView):
    queryset = User.objects.all()
    serializer_class = CustomRegisterSerializer


class UserDetailView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserDetailSerializer
    permission_classes = (IsAuthenticated,)
