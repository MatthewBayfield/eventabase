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
    
    # def address_validator(self):


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