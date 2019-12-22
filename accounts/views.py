from rest_auth.registration.views import RegisterView
from rest_auth.views import UserDetailsView
from rest_framework.permissions import AllowAny, IsAuthenticated

from accounts.models import User
from accounts.serializers import CustomUserDetailSerializer, CustomRegisterSerializer


# 유저 등록은 rest_auth의 RegisterView를 이용해 등록
from config.permission import IsOwner


class CustomRegisterView(RegisterView):
    queryset = User.objects.all()
    serializer_class = CustomRegisterSerializer
    permission_classes = (AllowAny,)


class UserDetailView(UserDetailsView):
    queryset = User.objects.all()
    serializer_class = CustomUserDetailSerializer
    permission_classes = (IsOwner,)
    # permission_classes = (IsAuthenticated,)

# class UserProfileView(RetrieveUpdateAPIView):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializer
#     permission_classes = (IsOwner,)
