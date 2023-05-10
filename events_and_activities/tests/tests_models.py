import datetime
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from allauth.account.models import EmailAddress
from landing_page.models import CustomUserModel
from home.models import UserAddress, UserProfile
from ..models import EventsActivities, Engagement


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
        expected_verbose_names = ['engagement', 'ID', 'title', 'host', 'status',
                                  'when', 'closing date', 'max no. of attendees',
                                  'keywords', 'description', 'requirements',
                                  'Address line 1',
                                  'City/Town',
                                  'County',
                                  'Postcode',
                                  'attendees']
        self.assertEqual(EventsActivities.retrieve_field_names(), expected_verbose_names)
        expected_names = ['engagement', 'id', 'title', 'host_user', 'status',
                          'when', 'closing_date',
                          'max_attendees', 'keywords', 'description',
                          'requirements', 'address_line_one', 'city_or_town',
                          'county', 'postcode', 'attendees']
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
        retrieved_verbose_data = new_event.retrieve_field_data()
        engagement_field = retrieved_verbose_data.pop('engagement')
        attendees_field = retrieved_verbose_data.pop('attendees')
        self.assertEqual(retrieved_verbose_data, expected_verbose_data)
        # should have no attendees
        self.assertEqual(engagement_field.count(), 0)
        self.assertEqual(attendees_field.count(), 0)
        expected_data = {'id': 1, 'host_user': user,
                         'status': 'advertised', 'title': 'Paintballing',
                         'when': datetime.datetime(2022, 12, 23, 12, 0),
                         'closing_date': datetime.datetime(2022, 12, 15, 12, 0),
                         'max_attendees': 20, 'keywords': 'outdoors,paintballing,competitive',
                         'description': 'Paintballing dayout, followed by lunch.',
                         'requirements': 'min £50 per person. wear suitable shoes. Need to be physically fit.',
                         'address_line_one': 'mayhem paintball', 'city_or_town': 'adbridge', 'county': 'essex',
                         'postcode': 'rm4 1AA'}
        retrieved_data = new_event.retrieve_field_data(False)
        engagement_field = retrieved_data.pop('engagement')
        attendees_field = retrieved_data.pop('attendees')
        self.assertEqual(retrieved_data, expected_data)
        # should have no attendees
        self.assertEqual(engagement_field.count(), 0)
        self.assertEqual(attendees_field.count(), 0)

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


class TestEngagementModel(TestCase):
    """
    Tests for the Engagement through model.
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
    data3 = {'email': 'tommypaul14788@gmail.com',
             'email2': 'tommypaul14788@gmail.com',
             'password1': 'holly!12345',
             'password2': 'holly!12345',
             'username': 'jimmy14798'}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Sign-up new users 
        client = Client()
        client.post('/accounts/signup/', cls.data)
        client.post('/accounts/signup/', cls.data2)
        client.post('/accounts/signup/', cls.data3)
        # verify user emails
        user_email = EmailAddress.objects.get(user='tommypaul147@gmail.com')
        user_email.verified = True
        user_email.save()
        user_email2 = EmailAddress.objects.get(user='tommypaul1478@gmail.com')
        user_email2.verified = True
        user_email2.save()
        user_email3 = EmailAddress.objects.get(user='tommypaul14788@gmail.com')
        user_email3.verified = True
        user_email3.save()

        cls.user = CustomUserModel.objects.get(username=cls.data['username'])
        cls.user2 = CustomUserModel.objects.get(username=cls.data2['username'])
        cls.user3 = CustomUserModel.objects.get(username=cls.data3['username'])
        cls.event1 = EventsActivities.objects.create(host_user=cls.user,
                                                     status="advertised",
                                                     title='event1',
                                                     when="2030-12-23 12:00:00",
                                                     closing_date="2025-10-15 12:00:00",
                                                     max_attendees=20,
                                                     keywords="outdoors,paintballing,competitive",
                                                     description="Paintballing dayout, followed by lunch.",
                                                     requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                                     address_line_one='mayhem paintball',
                                                     city_or_town='adbridge',
                                                     county='essex',
                                                     postcode='rm4 1AA')
        cls.event2 = EventsActivities.objects.create(host_user=cls.user2,
                                                     status="advertised",
                                                     title='event2',
                                                     when="2030-12-23 12:00:00",
                                                     closing_date="2025-10-15 12:00:00",
                                                     max_attendees=20,
                                                     keywords="outdoors,paintballing,competitive",
                                                     description="Paintballing dayout, followed by lunch.",
                                                     requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                                     address_line_one='mayhem paintball',
                                                     city_or_town='adbridge',
                                                     county='essex',
                                                     postcode='rm4 1AA')

    def test_engagement_instance_creation(self):
        """
        Tests that the engagement through model instance creation operates as expected when an attendee is added to an existing event.
        """
        self.assertEqual(Engagement.objects.count(), 0)
        # add interested attendees for event1 
        self.event1.attendees.add(self.user2, through_defaults={'status': 'In'})
        self.event1.attendees.add(self.user3, through_defaults={'status': 'In'})
        self.assertEqual(Engagement.objects.count(), 2)
        instances = [{'event': 1, 'user': 'jimmy14798', 'status': 'In'}, {'event': 1, 'user': 'jimmy1479', 'status': 'In'}]
        self.assertListEqual(list(Engagement.objects.filter(event=1).values('event', 'user', 'status')), instances)

        # add interested attendee for event2
        Engagement.objects.create(event=self.event2, user=self.user, status='In')
        instances = [{'event': 2, 'user': 'jimmy147', 'status': 'In'}]
        self.assertEqual(Engagement.objects.count(), 3)
        self.assertListEqual(list(Engagement.objects.filter(event=2).values('event', 'user', 'status')), instances)
    
    def test_engagement_instance_update(self):
        """
        Tests that the Engagement through model is updated as expected when an instance's status field is altered.
        """
        self.assertEqual(Engagement.objects.count(), 0)
        # add interested attendees for event1 and event2
        self.event1.attendees.add(self.user2, through_defaults={'status': 'In'})
        self.event2.attendees.add(self.user, through_defaults={'status': 'In'})
        # update status for event 1 and event 2 attendees
        time_created_event1 = Engagement.objects.filter(event=self.event1)[0].last_updated
        time_created_event2 = Engagement.objects.filter(event=self.event2)[0].last_updated
        Engagement.objects.update_or_create(user=self.user, event=self.event2, defaults={'status': 'Att'})
        self.event1.engagement.update_or_create(user=self.user2, defaults={'status': 'Attd'})
        self.assertEqual(Engagement.objects.count(), 2)
        instances = [{'event': 1, 'user': 'jimmy1479', 'status': 'Attd'}]
        self.assertListEqual(list(Engagement.objects.filter(event=1).values('event', 'user', 'status')), instances)
        instances = [{'event': 2, 'user': 'jimmy147', 'status': 'Att'}]
        self.assertListEqual(list(Engagement.objects.filter(event=2).values('event', 'user', 'status')), instances)
        # check last_updated fields have been updated as expected
        self.assertGreater(self.event1.engagement.get(user=self.user2).last_updated, time_created_event1)
        self.assertGreater(self.event2.engagement.get(user=self.user).last_updated, time_created_event1)

    def test_change_user_status_model_manager(self):
        """
        Tests the custom ChangeUserStatus model manager of the Engagement through model.
        """
        # add interested attendees for event1 
        self.event1.attendees.add(self.user2, through_defaults={'status': 'In'})
        self.event1.attendees.add(self.user3, through_defaults={'status': 'In'})
        # add interested attendee for event2
        Engagement.objects.create(event=self.event2, user=self.user, status='In')
        # Alter the closing date of event1 to a past date
        self.event1.closing_date = "2022-10-15 12:00:00"
        self.event1.save()
        # call the update_status manager method
        Engagement.user_status.update_status(self.user)
        Engagement.user_status.update_status(self.user2)
        Engagement.user_status.update_status(self.user3)
        for instance in self.event1.engagement.all():
            self.assertEqual(instance.status, 'Att')
        for instance in self.event2.engagement.all():
            self.assertEqual(instance.status, 'In')
        # Alter the closing date and the when date of event2 to a past date
        self.event2.closing_date = "2022-10-15 12:00:00"
        self.event2.when = "2023-01-23 12:00:00"
        self.event2.save()
        # call the update_status manager method
        Engagement.user_status.update_status(self.user)
        Engagement.user_status.update_status(self.user2)
        Engagement.user_status.update_status(self.user3)
        for instance in self.event1.engagement.all():
            self.assertEqual(instance.status, 'Att')
        for instance in self.event2.engagement.all():
            self.assertEqual(instance.status, 'Attd')
