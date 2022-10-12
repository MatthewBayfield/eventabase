import re
from django.db import models
from django.core.validators import (RegexValidator,
                                    MaxLengthValidator,
                                    DecimalValidator)
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
                                    verbose_name='username',
                                    to_field='username', primary_key=True,
                                    related_name='profile')
    
    first_name = models.CharField(max_length=50, verbose_name='first name',
                                  validators=[RegexValidator(regex=r"/^[a-z]+$/",
                                              message="Must contain only standard alphabetic characters.",
                                              flags=re.I),
                                              MaxLengthValidator(50)])
    last_name = models.CharField(max_length=50, verbose_name='last name',
                                 validators=[RegexValidator(regex=r"/^[a-z]+$/",
                                             message="Must contain only standard alphabetic characters.",
                                             flags=re.I),
                                             MaxLengthValidator(50)])

    date_of_birth = models.DateField(verbose_name='date of birth')
    SEX_CHOICES = [('male', 'male'), ('female', 'female')]
    sex = models.CharField(choices=SEX_CHOICES, max_length=10, verbose_name='sex')
    bio = models.TextField(max_length=250, default='', verbose_name='bio',
                           validators=[MaxLengthValidator(250)])

    objects = models.Manager()

    def retrieve_field_data(self):
        """
        Returns db field name-value pairs for a user profile instance as a dictionary.
        """
        fields = self._meta.get_fields()
        field_names = [field.name for field in fields]
        field_verbose_names = [(field.verbose_name if hasattr(field, 'verbose_name') else field.name) for field in fields]
        field_values = [getattr(self, field_name) for field_name in field_names]
        field_data = dict(zip(field_verbose_names, field_values))
        return field_data


class UserAddress(models.Model):
    """
    Model to store registered user addresses

     Attributes:
        username (character field)
        address_line_one (character field)
        city_or_town (character field)
        county (character field)
        postcode (character field): UK postcode for user's address
        latitude (decimal field): latitude of the user's address
        longitude (text field): longitude of user's address
    """
    username = models.OneToOneField(UserProfile, on_delete=models.CASCADE,
                                    to_field='username', primary_key=True,
                                    related_name='address')

    address_line_one = models.CharField(max_length=100, verbose_name='Address line 1',
                                        validators=[RegexValidator(regex=r"/[a-z0-9]+|([a-z0-9]?<=)\s(?=[a-z0-9])/",
                                                    message="Must contain only standard alphabetic characters and numbers.",
                                                    flags=[re.I, re.M]),
                                                    MaxLengthValidator(100)])
    
    city_or_town = models.CharField(max_length=50, verbose_name='City/Town',
                                    validators=[RegexValidator(regex=r"/[a-z]+|([a-z]?<=)\s(?=[a-z])/",
                                                               message="Must contain only standard alphabetic characters.",
                                                               flags=[re.I]),
                                                MaxLengthValidator(50)])
    
    county = models.CharField(max_length=50, verbose_name='County',
                              validators=[RegexValidator(regex=r"/[a-z]+|([a-z]?<=)\s(?=[a-z])/",
                                                         message="Must contain only standard alphabetic characters.",
                                                         flags=[re.I]),
                                          MaxLengthValidator(50)])
    
    # taken from https://stackoverflow.com/questions/164979/regex-for-matching-uk-postcodes/17024047#17024047
    UK_POSTCODE_REGREX_EXPRESSION = r"/^(([gG][iI][rR] {0,}0[aA]{2})|((([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y]?[0-9][0-9]?)|(([a-pr-uwyzA-PR-UWYZ][0-9][a-hjkstuwA-HJKSTUW])|([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y][0-9][abehmnprv-yABEHMNPRV-Y]))) {0,}[0-9][abd-hjlnp-uw-zABD-HJLNP-UW-Z]{2}))$/"

    postcode = models.CharField(max_length=10, verbose_name='Postcode',
                                validators=[RegexValidator(regex=UK_POSTCODE_REGREX_EXPRESSION,
                                                           message="Must be a valid postcode format."),
                                            MaxLengthValidator(10)])

    latitude = models.DecimalField(max_digits=8, decimal_places=4,
                                   validators=[DecimalValidator(8, 4)])

    longitude = models.DecimalField(max_digits=8, decimal_places=4,
                                    validators=[DecimalValidator(8, 4)])

    objects = models.Manager()

    def retrieve_field_data(self):
        """
        Returns db field name-value pairs for a user address instance as a dictionary.
        """
        fields = self._meta.get_fields()
        field_names = [field.name for field in fields]
        field_verbose_names = [(field.verbose_name if hasattr(field, 'verbose_name') else field.name) for field in fields]
        field_values = [getattr(self, field_name) for field_name in field_names]
        field_data = dict(zip(field_verbose_names, field_values))
        return field_data
