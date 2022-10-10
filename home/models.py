import re
from django.db import models
from django.core.validators import RegexValidator, MaxLengthValidator
from landing_page.models import CustomUserModel

# Create your models here.


class UserProfile(models.Model):
    """
    User profile model to store registered user personal information.

    Attributes:
        username (character field)
        first_name (character field)
        last_name (character field)
        date_of_birth (Date field)
        Sex (character field)
        Bio (text field): User biography.
    """
    username = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE,
                                    to_field='username', primary_key=True,
                                    related_name='profile')
    
    first_name = models.CharField(max_length=50, 
                                  validators=[RegexValidator(regex=r"/^[a-z]+$/",
                                              message="Must contain only standard alphabetic characters.",
                                              flags=re.I),
                                              MaxLengthValidator(50)])
    last_name = models.CharField(max_length=50,
                                 validators=[RegexValidator(regex=r"/^[a-z]+$/",
                                             message="Must contain only standard alphabetic characters.",
                                             flags=re.I),
                                             MaxLengthValidator(50)])

    date_of_birth = models.DateField()
    SEX_CHOICES = [('male', 'male'), ('female', 'female')]
    sex = models.CharField(choices=SEX_CHOICES, max_length=10)
    Bio = models.TextField(max_length=250, default='',
                           validators=[MaxLengthValidator(250)])

    objects = models.Manager()
