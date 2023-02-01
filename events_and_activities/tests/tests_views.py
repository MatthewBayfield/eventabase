from django.test import TestCase
from django.test import Client
from django.urls import reverse
from allauth.account.models import EmailAddress
from landing_page.models import CustomUserModel
from home.models import UserAddress, UserProfile
from ..forms import EventsActivitiesForm
from ..models import EventsActivities


class TestPostEventsView(TestCase):
    """
    Tests for PostEventsView.
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
    
    def test_get_response_authenticated_user(self):
        """
        Tests that the post events section template is rendered as part of an authenticated user's homepage.
        """
        client = Client()
        # sign-in user
        response = client.login(email=self.data['email'],
                                password=self.data['password1'])
        response = client.get('/home/')
        response_code = response.status_code
        self.assertEqual(response_code, 200)
        self.assertTemplateUsed('events_and_activities/post_events.html')

    def test_response_direct_get_request_post_events_view(self):
        """
        Tests that if a user tries to access the PostEventsView
        via a GET request to its url, they are redirected.
        """
        # unauthenticated user
        client = Client()
        response = client.get('/home/post_events/', follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/home/post_events/')
        # authenticated user
        client.login(email=self.data['email'],
                     password=self.data['password1'])
        response = client.get('/home/post_events/', follow=True)
        self.assertRedirects(response, '/home/')

    def test_post_events_modal_and_form_rendering(self):
        """
        Tests that the post events modal is rendered as expected, with a blank form instance.
        """
        client = Client()
        client.login(email=self.data['email'],
                     password=self.data['password1'])
        response = client.get('/home/')
        self.assertTemplateUsed(response, 'events_and_activities/post_events_modal.html')
        self.assertTemplateUsed(response, 'events_and_activities/post_events_form.html')
        sub_context = {'post_events_form': EventsActivitiesForm()}
        for key, value in sub_context.items():
            with self.subTest(key):
                self.assertHTMLEqual(str(response.context[key]), str(value))
        self.assertContains(response, str(EventsActivitiesForm()), html=True)

    def test_the_post_events_section_view_related_logic_and_rendering(self):
        """
        Tests PostEventsView GET method for generating the context for the post events section template and rendering the template.
        """
        user = CustomUserModel.objects.get(username=self.data['username'])
        user2 = CustomUserModel.objects.get(username=self.data2['username'])
        # create identical events varying in either their host, title, 'closing date' and or 'when' values.
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
                                        postcode='rm4 1aa')
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
                                        postcode='rm4 1aa')
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
                                        postcode='rm4 1aa')
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
                                        postcode='rm4 1aa')
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
                                        postcode='rm4 1aa')
        # expected data
        expected_advertised_event_data = [{'ID': 1, 'host': user, 'title': 'event1',
                                           'when': '12:00, 23/12/30', 'closing date': '12:00, 15/12/28',
                                           'max no. of attendees': 20, 'keywords': 'outdoors,paintballing,competitive',
                                           'description': 'Paintballing dayout, followed by lunch.',
                                           'requirements': 'min £50 per person. wear suitable shoes. Need to be physically fit.',
                                           'Address line 1': 'mayhem paintball', 'City/Town': 'adbridge',
                                           'County': 'essex', 'Postcode': 'rm4 1aa'}]
        expected_upcoming_event_data = [{'ID': 3, 'host': user, 'title': 'event3',
                                         'when': '12:00, 23/12/30', 'closing date': '12:00, 15/10/22',
                                         'max no. of attendees': 20, 'keywords': 'outdoors,paintballing,competitive',
                                         'description': 'Paintballing dayout, followed by lunch.',
                                         'requirements': 'min £50 per person. wear suitable shoes. Need to be physically fit.',
                                         'Address line 1': 'mayhem paintball', 'City/Town': 'adbridge',
                                         'County': 'essex', 'Postcode': 'rm4 1aa'}]
        client = Client()
        client.login(email=self.data['email'],
                     password=self.data['password1'])
        response = client.get('/home/')
        self.assertTemplateUsed(response, 'events_and_activities/post_section.html')
        sub_context = {'advertised_hosting_events_data': expected_advertised_event_data,
                       'upcoming_hosting_events_data': expected_upcoming_event_data}
        for key, value in sub_context.items():
            with self.subTest(key):
                self.assertEqual(response.context[key], value)
    
    def test_post_events_form_handling_and_processing(self):
        """
        Tests the POST method of the PostEventsView, that is responsible for handling the post events form submission.
        """
        event = {'status': 'advertised',
                 'title': 'paintballing',
                 'when': '13:30, 19/01/30',
                 'closing_date': '11:00, 01/01/30',
                 'max_attendees': 20,
                 'keywords': 'outdoors,fun',
                 'description': 'painballing then lunch.',
                 'requirements': '£50 per person',
                 'address_line_one': '58 StanLey Avenue',
                 'city_or_town': 'GIdea Park',
                 'county': 'ESSEX',
                 'postcode': 'Rm26Bt'}
        expected_rendered_event = '''<div class="event_container advertised" region role="region" aria-label="event" tabindex="0">
                                     <div><h5>No. of users attending: </h5><div class="details_display"><span>Id :</span><span>1</span>
                                     </div><div class="details_display"><span>Host :</span><span>jimmy147</span></div>
                                     <div class="details_display"><span>Title :</span><span>paintballing</span></div>
                                     <div class="details_display"><span>When :</span><span>13:30, 19/01/30</span>
                                     </div><div class="details_display"><span>Closing Date :</span><span>11:00, 01/01/30</span>
                                     </div><div class="details_display"><span>Max No. Of Attendees :</span><span>20</span>
                                     </div><div class="details_display"><span>Keywords :</span><span>outdoors,fun</span>
                                     </div><div class="details_display"><span>Description :</span><span>painballing then lunch.</span>
                                     </div><div class="details_display"><span>Requirements :</span><span>£50 per person</span>
                                     </div></div><div><div class="details_display"><span>Address Line 1 :</span>
                                     <span>58 Stanley Avenue</span></div><div class="details_display">
                                     <span>City/Town :</span><span>Gidea Park</span></div><div class="details_display">
                                     <span>County :</span><span>Essex</span></div><div class="details_display"><span>Postcode :</span>
                                     <span>rm26bt</span></div><button>Cancel</button><button>Message Attendees</button></div></div>'''
        # test for valid form:

        client = Client()
        # user sign-in
        client.login(email=self.data['email'],
                     password=self.data['password1'])
        event['host_user'] = CustomUserModel.objects.get(email=self.data['email'])
        # submit form
        response = client.post(reverse('home:post_events_view'), data=event, mode='same_origin')
        response_json = response.json()
        # check response 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['valid'], 'true')
        self.assertHTMLEqual(response_json['event'], expected_rendered_event)
        self.assertHTMLEqual(response_json['form'], str(EventsActivitiesForm()))
        # test for invalid form:

        client = Client()
        # user sign-in
        client.login(email=self.data['email'],
                     password=self.data['password1'])
        event['host_user'] = CustomUserModel.objects.get(email=self.data['email'])
        event['when'] = '13:30'
        new_form = EventsActivitiesForm(event)
        rendered_form = new_form.render(context=new_form.get_context())
        # submit form
        response = client.post(reverse('home:post_events_view'), data=event, mode='same_origin')
        response_json = response.json()
        # check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['valid'], 'false')
        self.assertHTMLEqual(response_json['form'], rendered_form)

        