from rest_auth.registration.views import RegisterView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from accounts.models import User
from accounts.serializers import CustomUserDetailSerializer, CustomRegisterSerializer


# 유저 등록은 rest_auth의 RegisterView를 이용해 등록
class CustomRegisterView(RegisterView):
    queryset = User.objects.all()
    serializer_class = CustomRegisterSerializer
    permission_classes = (AllowAny,)


class UserDetailView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserDetailSerializer
    permission_classes = (IsAuthenticated, )
