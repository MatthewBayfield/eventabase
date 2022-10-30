from django.forms.models import ModelForm
from django.forms.widgets import HiddenInput
from django.forms.fields import DateTimeField
from landing_page.forms import FormFieldMixin
from .models import EventsActivities
from .validators import check_date_has_not_occured, compare_dates


class EventsActivitiesForm(ModelForm, FormFieldMixin):
    """
    A Form for creating and posting new events
    """
    template_name = 'events_and_activities/post_events_form.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_field_styles()
    
    class Meta:
        model = EventsActivities
        fields = ['host_user', 'title', 'when', 'closing_date',
                  'max_attendees', 'keywords',
                  'description', 'requirements',
                  'address_line_one', 'city_or_town',
                  'county', 'postcode']
        widgets = {'host_user': HiddenInput()}
        error_messages = {'host_user': {'unique_for_date': 'You are already advertising or hosting an event on this date.'}}
        help_texts = {'keywords': 'Enter a comma separated list of descriptive keywords.',
                      'description': 'Describe the event or activity.',
                      'requirements': 'Detail any significant requirements for attending the event/activity, for example costs, travel arrangements, physical demands.'}

    when = DateTimeField(input_formats=["%H:%M, %d/%m/%y"], label='When',
                         help_text="Enter a date & time for the event: e.g. '07:30, 10/11/23'.",
                         error_messages={'invalid': 'Enter a valid datetime format.'},
                         validators=[check_date_has_not_occured])

    closing_date = DateTimeField(input_formats=["%H:%M, %d/%m/%y"], label='Closing Date',
                                 help_text="Enter a date & time when the advert should end: e.g. '07:30, 10/11/23'.",
                                 error_messages={'invalid': 'Enter a valid datetime format.'},
                                 validators=[check_date_has_not_occured])

    def clean(self):
        """
        Modified the modelform clean method to include 'closing_date' and 'when' datetime check.
        """
        self._validate_unique = True
        try:
            compare_dates(self.cleaned_data['closing_date'], self.cleaned_data['when'])
        except KeyError:
            return self.cleaned_data
        return self.cleaned_data

    def post_clean_processing(self):
        """
        Standardises cleaned field values.
        """
        processed_data = self.cleaned_data.copy()
        processed_data.update({field: value.title() for field, value in self.cleaned_data.items() if field in ['address_line_one', 'city_or_town', 'county']})
        processed_data['postcode'] = processed_data['postcode'].lower()
        for field, value in processed_data.items():
            setattr(self.instance, field, value)