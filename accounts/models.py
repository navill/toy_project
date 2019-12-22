from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    # 일반 회원가입은 rest_auth.registration.serializers.RegisterSerializer
    # & rest_auth.registration.views.RegisterView에 의해 이루어진다.
    def create_user(self, email, first_name, last_name, phone, password=None):
        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            last_name=last_name,
            first_name=first_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # def create_staffuser(self, email, phone, password):
    #     user = self.create_user(
    #         email,
    #         password=password,
    #         phone=phone,
    #     )
    #     user.staff = True
    #     user.save(using=self._db)
    #     return user

    # qwert4321@naver.com
    def create_superuser(self, email, first_name, last_name, phone, password):
        user = self.create_user(
            email,
            password=password,
            phone=phone,
            last_name=last_name,
            first_name=first_name,
        )
        user.staff = True
        user.admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=100)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    # customize user 생성 시 반드시 필요
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'last_name', 'first_name']

    def __str__(self):
        return self.email

    # customuser 생성 시 반드시 objects=manager() 설정
    # -> 없을 경우 login 시 에러 발생
    objects = UserManager()


class UserProfile(models.Model):
    user = models.ForeignKey(User, related_name='profiles', on_delete=models.CASCADE)
    address = models.CharField(max_length=100, null=True, blank=True)
