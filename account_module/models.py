import datetime

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from account_module.validaotrs import iran_phone_number_validator
from quiz_module.validators import is_valid_iran_code


class UserManager(BaseUserManager):
    def create_user(self, national_code, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError(_("the phone number must be set"))
        if not national_code:
            raise ValueError(_("the national_code must be set"))
        user = self.model(phone_number=phone_number, national_code=national_code, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, national_code, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(national_code, phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=255, verbose_name="نام و نام خانوادگی")
    national_code = models.CharField(max_length=10, unique=True, validators=[is_valid_iran_code], verbose_name='کد ملی')
    phone_number = models.CharField(max_length=13, unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "national_code"
    REQUIRED_FIELDS = ["phone_number"]

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = UserManager()

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return f"{self.full_name} ==> {self.national_code}"


class Otp(models.Model):
    phone_number = models.CharField(max_length=13)
    code = models.CharField(max_length=6)
    expires = models.DateTimeField()

    class Meta:
        verbose_name = 'کد یبار مصرف'
        verbose_name_plural = 'کدهای یبار مصرف'

    def is_valid_code(self):
        return datetime.datetime.now() <= self.expires

    def __str__(self):
        return f"{self.phone_number} ==> {self.code}"
