import re
from django.db import models
from django.core.validators import (RegexValidator,
                                    MaxLengthValidator,
                                    DecimalValidator)
from landing_page.models import CustomUserModel

# Create your models here.


class ProfileMixin(models.Model):
    """
    Abstract model. Contains methods common to multiple home app models, specifically for retrieving database field data.
    """
    class Meta:
        abstract = True

    @classmethod
    def retrieve_field_names(cls, verbose_names=True):
        """
        Returns the field names of a model as a list.

        Args:
            verbose_names (boolean): Indicates whether to return the verbose field names.
        """
        fields = cls._meta.get_fields()
        field_names = [field.name for field in fields]
        if verbose_names:
            field_verbose_names = [(field.verbose_name if hasattr(field, 'verbose_name') else field.name) for field in fields]
            return field_verbose_names
        return field_names

    def retrieve_field_data(self, verbose_names=True):
        """
        Returns db field name-value pairs for a user address instance as a dictionary.

        Args:
            verbose_names (boolean): Indicates whether to return the verbose field names in the dictionary.
        """
        field_names = self.retrieve_field_names(False)
        field_values = [getattr(self, field_name, None) for field_name in field_names]
        if verbose_names:
            field_verbose_names = self.retrieve_field_names()
            field_data = dict(zip(field_verbose_names, field_values))
            return field_data
        field_data = dict(zip(field_names, field_values))
        return field_data


class UserProfile(ProfileMixin):
    """
    User profile model to store registered user personal information.

    Attributes:
        user (One-To-One Field): one-to-one relationship with the CustomUserModel via the username field.
        first_name (character field)
        last_name (character field)
        date_of_birth (Date field)
        Sex (character field)
        Bio (text field): User biography.
    """
    user = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE,
                                verbose_name='user',
                                to_field='username', primary_key=True,
                                related_name='profile',
                                db_column='username')
    
    first_name = models.CharField(max_length=50, verbose_name='first name',
                                  validators=[RegexValidator(regex=r"/^[a-z]+$/",
                                              message="Must contain only standard alphabetic characters.",
                                              flags=re.I),
                                              MaxLengthValidator(50)],
                                  blank=False)
    last_name = models.CharField(max_length=50, verbose_name='last name',
                                 blank=False,
                                 validators=[RegexValidator(regex=r"/^[a-z]+$/",
                                             message="Must contain only standard alphabetic characters.",
                                             flags=re.I),
                                             MaxLengthValidator(50)])

    date_of_birth = models.DateField(verbose_name='date of birth',
                                     blank=False,)
    SEX_CHOICES = [('male', 'male'), ('female', 'female')]
    sex = models.CharField(choices=SEX_CHOICES, max_length=10, verbose_name='sex',
                           blank=False,)
    bio = models.TextField(max_length=500, default='', verbose_name='bio',
                           validators=[MaxLengthValidator(500)],
                           blank=True)

    objects = models.Manager()


class UserAddress(ProfileMixin):
    """
    Model to store registered user addresses

     Attributes:
        user_profile (one-to-one field): one-to-one relationship with the UserProfile model via the user field.
        address_line_one (character field)
        city_or_town (character field)
        county (character field)
        postcode (character field): UK postcode for user's address
        latitude (decimal field): latitude of the user's address
        longitude (text field): longitude of user's address
    """
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE,
                                        to_field='user', primary_key=True,
                                        related_name='address',
                                        verbose_name='user profile',
                                        db_column='profile')

    address_line_one = models.CharField(max_length=100, verbose_name='Address line 1',
                                        validators=[RegexValidator(regex=r"/[a-z0-9]+|([a-z0-9]?<=)\s(?=[a-z0-9])/",
                                                    message="Must contain only standard alphabetic characters and numbers.",
                                                    flags=[re.I, re.M]),
                                                    MaxLengthValidator(100)],
                                        blank=False)
    
    city_or_town = models.CharField(max_length=50, verbose_name='City/Town',
                                    validators=[RegexValidator(regex=r"/[a-z]+|([a-z]?<=)\s(?=[a-z])/",
                                                               message="Must contain only standard alphabetic characters.",
                                                               flags=[re.I]),
                                                MaxLengthValidator(50)],
                                    blank=False)
    
    county = models.CharField(max_length=50, verbose_name='County',
                              validators=[RegexValidator(regex=r"/[a-z]+|([a-z]?<=)\s(?=[a-z])/",
                                                         message="Must contain only standard alphabetic characters.",
                                                         flags=[re.I]),
                                          MaxLengthValidator(50)],
                              blank=False)
    
    # taken from https://stackoverflow.com/questions/164979/regex-for-matching-uk-postcodes/17024047#17024047
    UK_POSTCODE_REGREX_EXPRESSION = r"/^(([gG][iI][rR] {0,}0[aA]{2})|((([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y]?[0-9][0-9]?)|(([a-pr-uwyzA-PR-UWYZ][0-9][a-hjkstuwA-HJKSTUW])|([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y][0-9][abehmnprv-yABEHMNPRV-Y]))) {0,}[0-9][abd-hjlnp-uw-zABD-HJLNP-UW-Z]{2}))$/"

    postcode = models.CharField(max_length=10, verbose_name='Postcode', blank=False,
                                validators=[RegexValidator(regex=UK_POSTCODE_REGREX_EXPRESSION,
                                                           message="Must be a valid postcode format."),
                                            MaxLengthValidator(10)])

    latitude = models.DecimalField(max_digits=8, decimal_places=4,
                                   blank=False,
                                   validators=[DecimalValidator(8, 4)])

    longitude = models.DecimalField(max_digits=8, decimal_places=4,
                                    blank=False,
                                    validators=[DecimalValidator(8, 4)])

    objects = models.Manager()