from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=100)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'last_name', 'first_name']

    def __str__(self):
        return self.email

    # customuser 생성 시 반드시 objects=manager() 설정
    # -> 없을 경우 login 시 에러 발생
    objects = UserManager()


class UserProfile(models.Model):
    user = models.ForeignKey(User, related_name='profiles', on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
