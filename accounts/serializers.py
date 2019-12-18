from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers

from accounts.models import User


class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)

    # custom user를 만들 때 반드시 custom_signup 오버라이딩
    # -> 오버라이딩 하지 않을 경우 custom field의 값이 db에 데이터가 들어가지 않는다.
    def custom_signup(self, request, user):
        user.phone = self.validated_data.get('phone', '')
        user.save(update_fields=['first_name', 'last_name', 'phone'])

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'phone': self.validated_data.get('phone', ''),
        }


class CustomUserDetailSerializer(UserDetailsSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone')
        read_only_fields = ('email',)
