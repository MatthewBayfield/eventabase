from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import EmailValidator, MaxLengthValidator
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.utils import timezone


# Create your models here.


class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    """
    """
    username = models.CharField(max_length=150, unique=True,
                                help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                                validators=[UnicodeUsernameValidator(),
                                            MaxLengthValidator(150)])

    email = models.EmailField(primary_key=True, unique=True,
                              validators=[EmailValidator()])

    is_staff = models.BooleanField(default=False, help_text="Designates whether the user can log into this admin site.",)
    is_superuser = models.BooleanField(default=False, help_text="Designates whether this user should be treated as active.")
    is_active = models.BooleanField("active", default=True,
                                    help_text="Designates whether this user should be treated as active."
                                              "Unselect this instead of deleting accounts.")
    date_joined = models.DateTimeField("date joined", default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()
