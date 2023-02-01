from datetime import datetime
from django.test import TestCase
from landing_page.models import CustomUserModel
from ..forms import EventsActivitiesForm
from ..models import EventsActivities


class TestEventsActivitiesForm(TestCase):
    """
    Tests for the EventsActivities form.
    """
    event = {'status': 'advertised',
             'title': 'paintballing',
             'when': '13:30, 19/01/30',
             'closing_date': '11:00, 01/01/30',
             'max_attendees': 20,
             'keywords': 'outdoors,fun',
             'description': 'paintballing then lunch.',
             'requirements': '£50 per person',
             'address_line_one': '58 Stanley Avenue',
             'city_or_town': 'GIdea Park',
             'county': 'ESSEX',
             'postcode': 'Rm26Bt'}
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # create user
        username = 'taylor111'
        email = 'marktaylor@hotmail.com'
        password = 'alpha555'
        CustomUserModel.objects.create(username=username, email=email, password=password)
        user = CustomUserModel.objects.get(username='taylor111')
        cls.event.update({'host_user': user})

    def test_host_user_validators(self):
        """
        Tests that the title field validators are applied and expected errors added to the form context.
        """
        event = self.event.copy()
        # create event on same date
        EventsActivities.objects.create(host_user=self.event['host_user'],
                                        status="advertised",
                                        title='Paintballing',
                                        when="2030-01-19 13:30:00",
                                        closing_date="2029-12-15 12:00:00",
                                        max_attendees=20,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1AA')
        new_form = EventsActivitiesForm(data=event)
        valid = new_form.is_valid()
        self.assertFalse(valid)
        self.assertFormError(new_form, 'host_user', 'You are already advertising or hosting an event on this date.')
    
    def test_title_field_validators(self):
        """
        Tests that the title field validators are applied and expected errors added to the form context.
        """
        event = self.event.copy()
        # test regrex validator
        event['title'] = 'fun   activity'
        new_form = EventsActivitiesForm(data=event)
        valid = new_form.is_valid()
        self.assertFalse(valid)
        self.assertFormError(new_form, 'title', "Must contain only the characters [a-zA-Z0-9,.!/;:], with single spaces between words.")
        # test maxlength validator
        event['title'] = 101*'t'
        new_form = EventsActivitiesForm(data=event)
        valid = new_form.is_valid()
        self.assertFalse(valid)
        self.assertFormError(new_form, 'title', 'Ensure this value has at most 100 characters (it has 101).')
        
    def test_when_field_validators(self):
        """
        Tests that the when field validators are applied and expected errors added to the form context.
        """
        event = self.event.copy()
        event['when'] = '19/11/93'
        new_form = EventsActivitiesForm(data=event)
        valid = new_form.is_valid()
        self.assertFalse(valid)
        self.assertFormError(new_form, 'when', 'Enter a valid datetime format.')
        event['when'] = '11:00, 01/01/93'
        new_form = EventsActivitiesForm(data=event)
        valid = new_form.is_valid()
        self.assertFalse(valid)
        self.assertFormError(new_form, 'when', 'This date and time is in the past.')
    
    def test_closing_date_field_validators(self):
        """
        Tests that the closing_date field validators are applied and expected errors added to the form context.
        """
        event = self.event.copy()
        event['closing_date'] = '11:00'
        new_form = EventsActivitiesForm(data=event)
        valid = new_form.is_valid()
        self.assertFalse(valid)
        self.assertFormError(new_form, 'closing_date', 'Enter a valid datetime format.')
        event['closing_date'] = '01:17, 29/10/20'
        new_form = EventsActivitiesForm(data=event)
        valid = new_form.is_valid()
        self.assertFalse(valid)
        self.assertFormError(new_form, 'closing_date', 'This date and time is in the past.')

    def test_keywords_field_validators(self):
        """
        Tests that the keywords field validators are applied and expected errors added to the form context.
        """
        event = self.event.copy()
        # test regrex validator
        event['keywords'] = 'fun, outdoors'
        new_form = EventsActivitiesForm(data=event)
        valid = new_form.is_valid()
        self.assertFalse(valid)
        self.assertFormError(new_form, 'keywords', "Must contain comma separated words containing only the characters [a-zA-Z0-9], with no spaces.")
        # test maxlength validator
        event['keywords'] = 76*'t'
        new_form = EventsActivitiesForm(data=event)
        valid = new_form.is_valid()
        self.assertFalse(valid)
        self.assertFormError(new_form, 'keywords', 'Ensure this value has at most 75 characters (it has 76).')

    def test_description_field_validators(self):
        """
        Tests that the description field validators are applied and expected errors added to the form context.
        """
        event = self.event.copy()
        # test maxlength validator
        event['description'] = 501*'t'
        new_form = EventsActivitiesForm(data=event)
        valid = new_form.is_valid()
        self.assertFalse(valid)
        self.assertFormError(new_form, 'description', 'Ensure this value has at most 500 characters (it has 501).')

    def test_requirements_field_validators(self):
        """
        Tests that the requirements field validators are applied and expected errors added to the form context.
        """
        event = self.event.copy()
        # test maxlength validator
        event['requirements'] = 501*'t'
        new_form = EventsActivitiesForm(data=event)
        valid = new_form.is_valid()
        self.assertFalse(valid)
        self.assertFormError(new_form, 'requirements', 'Ensure this value has at most 500 characters (it has 501).')

    def test_address_line_one_field_validators(self):
        """
        Tests that the address_line_one validators are applied and expected errors added to the form context.
        """
        event = self.event.copy()
        # test regrex validator
        event['address_line_one'] = '11 rise park     boulevard'
        new_form = EventsActivitiesForm(data=event)
        valid = new_form.is_valid()
        self.assertFalse(valid)
        self.assertFormError(new_form, 'address_line_one', "Must contain only standard alphabetic characters and numbers, with single spaces between words.")
        # test maxlength validator
        event['address_line_one'] = 101*'t'
        new_form = EventsActivitiesForm(data=event)
        valid = new_form.is_valid()
        self.assertFalse(valid)
        self.assertFormError(new_form, 'address_line_one', 'Ensure this value has at most 100 characters (it has 101).')

    def test_city_or_town_field_validators(self):
        """
        Tests that the city_or_town field validators are applied and expected errors added to the form context.
        """
        event = self.event.copy()
        # test regrex validator
        event['city_or_town'] = 'dageham3'
        new_form = EventsActivitiesForm(data=event)
        valid = new_form.is_valid()
        self.assertFalse(valid)
        self.assertFormError(new_form, 'city_or_town', "Must contain only standard alphabetic characters, with single spaces between words.")
        # test maxlength validator
        event['city_or_town'] = 51*'t'
        new_form = EventsActivitiesForm(data=event)
        valid = new_form.is_valid()
        self.assertFalse(valid)
        self.assertFormError(new_form, 'city_or_town', 'Ensure this value has at most 50 characters (it has 51).')

    def test_county_field_validators(self):
        """
        Tests that the county field validators are applied and expected errors added to the form context.
        """
        event = self.event.copy()
        # test regrex validator
        event['county'] = 'esse  x'
        new_form = EventsActivitiesForm(data=event)
        valid = new_form.is_valid()
        self.assertFalse(valid)
        self.assertFormError(new_form, 'county', "Must contain only standard alphabetic characters, with single spaces between words.")
        # test maxlength validator
        event['county'] = 51*'t'
        new_form = EventsActivitiesForm(data=event)
        valid = new_form.is_valid()
        self.assertFalse(valid)
        self.assertFormError(new_form, 'county', 'Ensure this value has at most 50 characters (it has 51).')

    def test_postcode_field_validators(self):
        """
        Tests that the postcode field validators are applied and expected errors added to the form context.
        """
        event = self.event.copy()
        # test regrex validator
        event['postcode'] = 'r345 6pl'
        new_form = EventsActivitiesForm(data=event)
        valid = new_form.is_valid()
        self.assertFalse(valid)
        self.assertFormError(new_form, 'postcode', "Must be a valid postcode format.")

    def test_compare_dates_validator(self):
        '''
        Tests the compare_dates validator.
        '''
        date1 = "13:30, 01/01/31"
        date2 = "13:31, 01/01/31"
        event = self.event.copy()
        event['closing_date'] = date2
        event['when'] = date1
        new_form = EventsActivitiesForm(data=event)
        valid = new_form.is_valid()
        self.assertFalse(valid)
        self.assertEqual(new_form.non_field_errors(), ['The closing advert date and time cannot be after when the event occurs.'])
        # switch dates
        event['closing_date'] = date1
        event['when'] = date2
        new_form = EventsActivitiesForm(data=event)
        valid = new_form.is_valid()
        self.assertTrue(valid)
        self.assertEqual(new_form.non_field_errors(), [])

    def test_required_field_validators(self):
        """
        Tests that an error is raised when a required field is left empty.
        """
        form = EventsActivitiesForm({})
        for field_name, field in form.fields.items():
            if field.required:
                self.assertFormError(form, field_name, ['This field is required.'])
            else:
                self.assertNotIn(field_name, form.errors)
    
    def test_set_field_styles_method(self):
        """
        Ensures the set_field_styles method works.
        """
        event = {'host_user': self.event['host_user'],
                 'status': 'advertise',
                 'title': 'paintballing@',
                 'when': '13:30, 19/01/23',
                 'closing_date': '20:00, 01/01/23',
                 'max_attendees': 20,
                 'keywords': 'outdoors,f  un',
                 'description': 'paintballing then lunch.',
                 'requirements': '£50 per person',
                 'address_line_one': '58 S!tanley Avenue',
                 'city_or_town': 'GIdea   Park',
                 'county': 'ESSEX45',
                 'postcode': 'Rm2z6Bt'}
        new_form = EventsActivitiesForm(data=event)
        visible_fields = new_form.visible_fields()
        for field in visible_fields:
            with self.subTest(field.name):
                if field.name in new_form.errors:
                    self.assertEqual(field.css_classes, 'form_fields errors_present')
                else:
                    self.assertEqual(field.css_classes, 'form_fields')

    def test_the_post_clean_processing_method(self):
        """
        Tests the method works.
        """
        event = {'host_user': self.event['host_user'],
                 'status': 'advertised',
                 'title': 'paintballing',
                 'when': '13:30, 19/01/31',
                 'closing_date': '11:00, 01/01/31',
                 'max_attendees': 20,
                 'keywords': 'outdoors,fun',
                 'description': 'painballing then lunch.',
                 'requirements': '£50 per person',
                 'address_line_one': '58 StanLey Avenue',
                 'city_or_town': 'GIdea Park',
                 'county': 'ESSEX',
                 'postcode': 'Rm26Bt'}
        
        post_processed_data = {'host_user': self.event['host_user'],
                               'status': 'advertised',
                               'title': 'paintballing',
                               'when': datetime.strptime('13:30, 19/01/31', "%H:%M, %d/%m/%y"),
                               'closing_date': datetime.strptime('11:00, 01/01/31', "%H:%M, %d/%m/%y"),
                               'max_attendees': 20,
                               'keywords': 'outdoors,fun',
                               'description': 'painballing then lunch.',
                               'requirements': '£50 per person',
                               'address_line_one': '58 Stanley Avenue',
                               'city_or_town': 'Gidea Park',
                               'county': 'Essex',
                               'postcode': 'rm26bt'}
        # create valid form from address dict
        new_form = EventsActivitiesForm(data=event)
        # check form is valid
        valid = new_form.is_valid()
        self.assertTrue(valid)
        new_form.post_clean_processing()
        for field_name, value in post_processed_data.items():
            received = getattr(new_form.instance, field_name)
            self.assertEqual(received, value)

    def test_event_form_instance_creation(self):
        """
        Tests that a new EventActivities instance is created as expected when using a valid form.
        """
        # assert the event does not already exist
        event = self.event.copy()
        self.assertFalse(EventsActivities.objects.filter(host_user=event['host_user'], when=datetime.strptime(event['when'], "%H:%M, %d/%m/%y")).exists())
        # create valid form
        new_form = EventsActivitiesForm(data=event)
        # check form is valid, as it should be.
        valid = new_form.is_valid()
        print(new_form.errors)
        self.assertTrue(valid)
        new_form.post_clean_processing()
        # save the instance and check it now exits    
        new_form.save()
        self.assertTrue(EventsActivities.objects.filter(host_user=event['host_user'], when=datetime.strptime(event['when'], "%H:%M, %d/%m/%y")).exists())

