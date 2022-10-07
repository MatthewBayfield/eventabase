from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import EmailValidator, MaxLengthValidator
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.utils import timezone


# Create your models here.


class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for user account creation and user authentication.

    Inherits password and last_login model fields from AbstractBaseUser.

    Attributes:
        username (character field)
        email (character field)
        is_staff (boolean field): indicates whether the user is a
                                  site administrator.
        is_superuser (boolean field): indicates whether the user has
                                       all permissions.
        is_active (boolean field): indicates if the account is active.
        date_joined (Date-time field): specifies when the user signed-up.
        USERNAME_FIELD (str): specifies name of field that acts as username.
        REQUIRED_FIELDS (str): specifies required fields other than password and USERNAME-FIELD.
        objects (obj): model user manager instance.


    """
    username = models.CharField(max_length=150, unique=True,
                                help_text="Required. 150 characters or fewer."
                                          "Letters, digits and @/./+/-/_ only.",
                                validators=[UnicodeUsernameValidator(),
                                            MaxLengthValidator(150)],
                                error_messages={'unique': 'A user with this username already exists.'})

    email = models.EmailField(primary_key=True, unique=True,
                              validators=[EmailValidator(), MaxLengthValidator(254, 'Email cannot be more than 254 characters.')])

    is_staff = models.BooleanField(default=False, help_text="Designates whether the user can log into this admin site.",)
    is_superuser = models.BooleanField(default=False, help_text="Designates that this user has all permissions without "
                                                                "explicitly assigning them.")
    is_active = models.BooleanField("active", default=True,
                                    help_text="Designates whether this user should be treated as active."
                                              "Unselect this instead of deleting accounts.")
    date_joined = models.DateTimeField("date joined", default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        db_table = 'registered_users'
