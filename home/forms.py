import os
import re
from pprint import pprint
from urllib.parse import quote
import requests
from requests.structures import CaseInsensitiveDict
from django.forms.models import ModelForm
from django.forms.fields import DateField
from home.models import UserProfile, UserAddress
from landing_page.forms import FormFieldMixin


class EditAddress(ModelForm, FormFieldMixin):
    """
    User Address model form.
    
    Allows a user to complete the address section of the edit profile modal form,
    when adding/editing their profile details. Uses fields from the UserAddress model.

    Attributes:
        template_name (str): form template.

    """
    template_name = 'home/edit_profile_form.html'
    
    class Meta:
        model = UserAddress
        fields = ['address_line_one', 'city_or_town', 'county',
                  'postcode']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_field_styles()
    
    def post_clean_processing(self, user_profile):
        """
        Standardises cleaned field values, and adds remaining fields for model instance creation.

        Args:
            user_profile (obj): a UserProfile model instance.
        """
        # user_address_field_regrex = {'address_line_one': r"^([a-zA-Z0-9]+\s{0,1}[a-zA-Z0-9]+)+\Z",
        #                 'city_or_town': r"^([a-zA-Z0-9]+\s{0,1}[a-zA-Z0-9]+)+\Z",
        #                 'county': r"^([a-zA-Z0-9]+\s{0,1}[a-zA-Z0-9]+)+\Z",
        #                 'postcode': r"^(([gG][iI][rR] {0,}0[aA]{2})|((([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y]?[0-9][0-9]?)|(([a-pr-uwyzA-PR-UWYZ][0-9][a-hjkstuwA-HJKSTUW])|([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y][0-9][abehmnprv-yABEHMNPRV-Y]))) {0,}[0-9][abd-hjlnp-uw-zABD-HJLNP-UW-Z]{2}))$"
        #                }
        processed_data = {field: value.lower() for field, value in self.cleaned_data.items()}
        for field, value in processed_data.items():
            setattr(self.instance, field, value)
        self.instance.user_profile = user_profile

    def set_coordintes(self):
        """
        Obtains latitude and longitude coordinates for a user address using the Geoapify API.
        """
        # Retrieve user address data from the submitted EditAddress form.
        address_terms = [getattr(self.instance, field_name) for field_name in self.cleaned_data.keys()]
        API_KEY = os.environ.get('GEOAPIFY_API_KEY')
        text_param = ', '.join(address_terms)
        text_param_url_safe = quote(text_param)
        url = f'https://api.geoapify.com/v1/geocode/search?text={text_param_url_safe}&lang=en&filter=countrycode:gb&format=json&apiKey={API_KEY}'
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"

        response = requests.get(url, headers=headers)
        # First result used. Accuracy very much depends on the provided user address validity. May filter results further in the future.
        first_result = response.json()['results'][0]
        latitude = round(float(first_result['lat']), 4)
        longitude = round(float(first_result['lon']), 4)
        self.instance.latitude = latitude
        self.instance.longitude = longitude


class EditPersonalInfo(ModelForm, FormFieldMixin):
    """
    User personal info model form.
    
    Allows a user to complete the personal info section of the edit profile modal form,
    when adding/editing their profile details. Uses fields from the UserProfile model.

    Attributes:
        template_name (str): form template.
        date_of_birth (date field): date of birth of user.
    """
    template_name = 'home/edit_profile_form.html'

    date_of_birth = DateField(input_formats=['%d/%m/%Y'], label='Date of Birth',
                              help_text='Enter a date in the format dd/mm/yyyy.',
                              error_messages={'invalid': 'Enter a valid date format.'})

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'date_of_birth',
                  'sex', 'bio']
        help_texts = {'bio': 'Describe a bit about yourself, and or the activities you like. Max 500 characters.'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_field_styles()

    def post_clean_processing(self, user):
        """
        Standardises cleaned field values, and adds remaining fields for model instance creation.

        Args:
            user (obj): a CustomUserModel model instance.
        """
        processed_data = self.cleaned_data.copy()
        processed_data.update({field: value.lower() for field, value in self.cleaned_data.items() if field in ['first_name', 'last_name']})
        for field, value in processed_data.items():
            setattr(self.instance, field, value)
        self.instance.user = user