import datetime
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from allauth.account.models import EmailAddress
from landing_page.models import CustomUserModel
from home.models import UserAddress, UserProfile
from ..models import EventsActivities


class TestEventsActivitiesModel(TestCase):
    """
    Tests for the EventsActivities model.
    """
    data = {'email': 'tommypaul147@gmail.com',
            'email2': 'tommypaul147@gmail.com',
            'password1': 'holly!123',
            'password2': 'holly!123',
            'username': 'jimmy147'}

    data2 = {'email': 'tommypaul1478@gmail.com',
             'email2': 'tommypaul1478@gmail.com',
             'password1': 'holly!1234',
             'password2': 'holly!1234',
             'username': 'jimmy1479'}
    
    info = {'first_name': 'mark',
            'last_name': 'taylor',
            'date_of_birth': '19/11/1993',
            'sex': 'male',
            'bio': 'I like sports'}
    address = {'address_line_one': '58 Stanley Avenue',
               'city_or_town': 'GIdea Park',
               'county': 'ESSEX',
               'postcode': 'Rm26Bt'}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Sign-up new users 
        client = Client()
        client.post('/accounts/signup/', cls.data)
        client.post('/accounts/signup/', cls.data2)
        # verify user emails
        user_email = EmailAddress.objects.get(user='tommypaul147@gmail.com')
        user_email.verified = True
        user_email.save()
        user_email2 = EmailAddress.objects.get(user='tommypaul1478@gmail.com')
        user_email2.verified = True
        user_email2.save()
        # create profile for user
        user = CustomUserModel.objects.get(email=user_email.email)
        UserProfile.objects.create(user=user,
                                   first_name='jimmy',
                                   last_name='knighton',
                                   date_of_birth='1926-03-25',
                                   sex='male',
                                   bio='I enjoy all outdoor activities.')
        # create address for user
        UserAddress.objects.create(user_profile=user.profile,
                                   address_line_one='57 portland gardens',
                                   city_or_town='chadwell heath',
                                   county='essex',
                                   postcode='rm65uh',
                                   latitude=51.5791,
                                   longitude=0.1355)
    
    def test_new_event_creation(self):
        """
        Tests that a new event/activity is created as expected
        """
        user = CustomUserModel.objects.get(username=self.data['username'])
        # create event/activity
        EventsActivities.objects.create(host_user=user,
                                        status="advertised",
                                        title='Paintballing',
                                        when="2022-12-23 12:00:00",
                                        closing_date="2022-12-15 12:00:00",
                                        max_attendees=20,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1AA')
        self.assertTrue((EventsActivities.objects.filter(host_user=user, title='Paintballing')).exists())
        new_event = EventsActivities.objects.filter(host_user=user, title='Paintballing')[0]
        self.assertEqual(new_event.max_attendees, 20)
        self.assertEqual(new_event.status, 'advertised')
        self.assertEqual(new_event.keywords, "outdoors,paintballing,competitive")
        self.assertEqual(str(new_event.when), "2022-12-23 12:00:00")
        self.assertEqual(str(new_event.closing_date), "2022-12-15 12:00:00")
        self.assertEqual(new_event.description, "Paintballing dayout, followed by lunch.")
        self.assertEqual(new_event.requirements, "min £50 per person. wear suitable shoes. Need to be physically fit.")
        self.assertEqual(new_event.address_line_one, 'mayhem paintball')
        self.assertEqual(new_event.city_or_town, 'adbridge')
        self.assertEqual(new_event.county, 'essex')
        self.assertEqual(new_event.postcode, 'rm4 1AA')

    def test_inherited_mixin_methods(self):
        """
        Tests that the ProfileMixin methods work as expected for the EventsActivities model.
        """
        # testing retrieve_field_names class method
        expected_verbose_names = ['ID', 'host', 'status', 'title',
                                  'when', 'closing date', 'max no. of attendees',
                                  'keywords', 'description', 'requirements',
                                  'Address line 1',
                                  'City/Town',
                                  'County',
                                  'Postcode']
        self.assertEqual(EventsActivities.retrieve_field_names(), expected_verbose_names)
        expected_names = ['id', 'host_user', 'status',
                          'title', 'when', 'closing_date',
                          'max_attendees', 'keywords', 'description',
                          'requirements', 'address_line_one', 'city_or_town',
                          'county', 'postcode']
        self.assertEqual(EventsActivities.retrieve_field_names(False), expected_names)
        # testing retrieve_field_data method
        user = CustomUserModel.objects.get(username=self.data['username'])
        EventsActivities.objects.create(host_user=user,
                                        status="advertised",
                                        title='Paintballing',
                                        when="2022-12-23 12:00:00",
                                        closing_date="2022-12-15 12:00:00",
                                        max_attendees=20,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1AA')
        new_event = EventsActivities.objects.filter(host_user=user, title='Paintballing')[0]
        expected_verbose_data = {'ID': 1, 'host': user, 'status': 'advertised',
                                 'title': 'Paintballing', 'when': datetime.datetime(2022, 12, 23, 12, 0),
                                 'closing date': datetime.datetime(2022, 12, 15, 12, 0),
                                 'max no. of attendees': 20,
                                 'keywords': 'outdoors,paintballing,competitive',
                                 'description': 'Paintballing dayout, followed by lunch.',
                                 'requirements': 'min £50 per person. wear suitable shoes. Need to be physically fit.',
                                 'Address line 1': 'mayhem paintball', 'City/Town': 'adbridge', 'County': 'essex',
                                 'Postcode': 'rm4 1AA'}
        self.assertEqual(new_event.retrieve_field_data(), expected_verbose_data)
        expected_data = {'id': 1, 'host_user': user,
                         'status': 'advertised', 'title': 'Paintballing',
                         'when': datetime.datetime(2022, 12, 23, 12, 0),
                         'closing_date': datetime.datetime(2022, 12, 15, 12, 0),
                         'max_attendees': 20, 'keywords': 'outdoors,paintballing,competitive',
                         'description': 'Paintballing dayout, followed by lunch.',
                         'requirements': 'min £50 per person. wear suitable shoes. Need to be physically fit.',
                         'address_line_one': 'mayhem paintball', 'city_or_town': 'adbridge', 'county': 'essex',
                         'postcode': 'rm4 1AA'}
        self.assertEqual(new_event.retrieve_field_data(False), expected_data)

    def test_change_expired_events_manager_with_no_user_param(self):
        """
        Tests the manager methods work as expected when no user param is given.
        """
        user = CustomUserModel.objects.get(username=self.data['username'])
        # create identical events varying in either their title, 'closing date' and or 'when' values.
        EventsActivities.objects.create(host_user=user,
                                        status="advertised",
                                        title='event1',
                                        when="2030-12-23 12:00:00",
                                        closing_date="2028-12-15 12:00:00",
                                        max_attendees=20,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1AA')
        EventsActivities.objects.create(host_user=user,
                                        status="advertised",
                                        title='event2',
                                        when="2022-10-30 12:00:00",
                                        closing_date="2022-10-15 12:00:00",
                                        max_attendees=20,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1AA')
        EventsActivities.objects.create(host_user=user,
                                        status="advertised",
                                        title='event3',
                                        when="2030-12-23 12:00:00",
                                        closing_date="2022-10-15 12:00:00",
                                        max_attendees=20,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1AA')
        all_events = EventsActivities.objects.all()
        self.assertEqual(len(all_events), 3)
        deleted = EventsActivities.expired.delete_expired()
        self.assertEqual(deleted[0], 1)
        self.assertFalse(EventsActivities.objects.filter(title='event2').exists())
        all_events = EventsActivities.objects.all()
        self.assertEqual(len(all_events), 2)
        EventsActivities.expired.update_expired()
        EventsActivities.objects.filter(status='confirmed')
        self.assertEqual(len(EventsActivities.objects.filter(status='confirmed')), 1)
        self.assertTrue(EventsActivities.objects.filter(status='confirmed', title='event3').exists())
        
    def test_change_expired_events_manager_with_user_param(self):
        """
        Tests the manager methods work as expected when user param is given.
        """
        user = CustomUserModel.objects.get(username=self.data['username'])
        user2 = CustomUserModel.objects.get(username=self.data2['username'])
        # create identical events varying in either their title, 'closing date' and or 'when' values.
        EventsActivities.objects.create(host_user=user,
                                        status="advertised",
                                        title='event1',
                                        when="2030-12-23 12:00:00",
                                        closing_date="2028-12-15 12:00:00",
                                        max_attendees=20,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1AA')
        EventsActivities.objects.create(host_user=user,
                                        status="advertised",
                                        title='event2',
                                        when="2022-10-30 12:00:00",
                                        closing_date="2022-10-15 12:00:00",
                                        max_attendees=20,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1AA')
        EventsActivities.objects.create(host_user=user,
                                        status="advertised",
                                        title='event3',
                                        when="2030-12-23 12:00:00",
                                        closing_date="2022-10-15 12:00:00",
                                        max_attendees=20,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1AA')
        EventsActivities.objects.create(host_user=user2,
                                        status="advertised",
                                        title='event4',
                                        when="2030-12-23 12:00:00",
                                        closing_date="2022-10-15 12:00:00",
                                        max_attendees=20,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1AA')
        EventsActivities.objects.create(host_user=user2,
                                        status="advertised",
                                        title='event5',
                                        when="2022-10-30 12:00:00",
                                        closing_date="2022-10-15 12:00:00",
                                        max_attendees=20,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1AA')
        all_events = EventsActivities.objects.all()
        self.assertEqual(len(all_events), 5)
        deleted = EventsActivities.expired.delete_expired(user)
        self.assertEqual(deleted[0], 1)
        self.assertFalse(EventsActivities.objects.filter(title='event2').exists())
        all_events = EventsActivities.objects.all()
        self.assertEqual(len(all_events), 4)
        EventsActivities.expired.update_expired(user)
        EventsActivities.objects.filter(status='confirmed')
        self.assertEqual(len(EventsActivities.objects.filter(status='confirmed')), 1)
        self.assertTrue(EventsActivities.objects.filter(status='confirmed', title='event3').exists())
        




