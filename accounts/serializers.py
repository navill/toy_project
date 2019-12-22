from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from accounts.models import User, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # , default=serializers.CurrentUserDefault())

    class Meta:
        model = UserProfile
        fields = ('user', 'address')
        # read_only_fields = ('user',)


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
            'last_name': self.validated_data.get('last_name', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'phone': self.validated_data.get('phone', ''),
        }

    # def create(self, validated_data):
    #     profiles = validated_data.pop('profiles')
    #     user = User.objects.create(**validated_data)
    #
    #     for profile in profiles:
    #         UserProfile.objects.create(user=user, **profile)
    #     return user


class CustomUserDetailSerializer(serializers.ModelSerializer):
    # profiles = UserProfileSerializer(many=True)
    profiles = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'profiles')
        read_only_fields = ('email',)

    def to_representation(self, instance):
        data = super(CustomUserDetailSerializer, self).to_representation(instance)
        print(data)
        profile = UserProfile.objects.get_or_create(user=instance)
        serializer = UserProfileSerializer(profile)
        data.update({'profiles': serializer.data})
        return data

    def update(self, instance, validated_data):
        profiles_data = validated_data.pop('profiles')

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()

        profile = UserProfile.objects.get_or_create(user_id=instance.id)
        for _, profile_data in profiles_data.items():
            profile[0].address = profile_data
        profile[0].save()

        return instance
