import re, json
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.core import mail
from django.template.loader import render_to_string
from eventabase.settings import EMAIL_HOST_USER
from allauth.account.models import EmailAddress
from landing_page.models import CustomUserModel
from home.models import UserAddress, UserProfile
from ..forms import EventsActivitiesForm
from ..models import EventsActivities, Engagement
from ..exceptions import EventClash


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
        expected_advertised_event_data = [({'ID': 1, 'host': user, 'title': 'event1',
                                           'when': '12:00, 23/12/30', 'closing date': '12:00, 15/12/28',
                                           'max no. of attendees': 20, 'keywords': 'outdoors,paintballing,competitive',
                                           'description': 'Paintballing dayout, followed by lunch.',
                                           'requirements': 'min £50 per person. wear suitable shoes. Need to be physically fit.',
                                           'Address line 1': 'mayhem paintball', 'City/Town': 'adbridge',
                                           'County': 'essex', 'Postcode': 'rm4 1aa'}, 0)]
        expected_upcoming_event_data = [({'ID': 3, 'host': user, 'title': 'event3',
                                         'when': '12:00, 23/12/30', 'closing date': '12:00, 15/10/22',
                                         'max no. of attendees': 20, 'keywords': 'outdoors,paintballing,competitive',
                                         'description': 'Paintballing dayout, followed by lunch.',
                                         'requirements': 'min £50 per person. wear suitable shoes. Need to be physically fit.',
                                         'Address line 1': 'mayhem paintball', 'City/Town': 'adbridge',
                                         'County': 'essex', 'Postcode': 'rm4 1aa'}, 0)]
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
        expected_rendered_event = '''<div class="event_container advertised" role="region" aria-label="event item" tabindex="0">
                                     <div><div class="details_display"><span>Id :</span><span>1.</span>
                                     </div><div class="details_display"><span>Title :</span><span>paintballing.</span></div>
                                     <div class="details_display"><span>Host :</span><span>jimmy147.</span></div>
                                     <div class="details_display"><span>When :</span><span>13:30, 19/01/30.</span>
                                     </div><div class="details_display"><span>Closing Date :</span><span>11:00, 01/01/30.</span>
                                     </div><div class="details_display"><span>Max No. Of Attendees :</span><span>20.</span>
                                     </div><div class="details_display"><span>Keywords :</span><span>outdoors,fun.</span>
                                     </div><div class="details_display"><span>Description :</span><span>painballing then lunch..</span>
                                     </div><div class="details_display"><span>Requirements :</span><span>£50 per person.</span>
                                     </div></div><div><div class="details_display"><span>Address Line 1 :</span>
                                     <span>58 Stanley Avenue.</span></div><div class="details_display">
                                     <span>City/Town :</span><span>Gidea Park.</span></div><div class="details_display">
                                     <span>County :</span><span>Essex.</span></div><div class="details_display"><span>Postcode :</span>
                                     <span>rm26bt.</span></div><h5 aria-label="number of users attending so far">No. of users attending so far: 0.</h5>
                                     <button class='delete_advert'>Delete Advert</button></div></div>'''
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
        msg = '<p class="errorlist"><strong>Please correct the errors described/indicated below, before resubmitting the form:</strong></p>'
        self.assertInHTML(msg, response_json['form'], count=0)
        # test for invalid form:

        client = Client()
        # user sign-in
        client.login(email=self.data['email'],
                     password=self.data['password1'])
        event['host_user'] = CustomUserModel.objects.get(email=self.data['email'])
        event['when'] = '13:30'
        new_form = EventsActivitiesForm(event)
        context = new_form.get_context()
        context.update({'errors_present': True})
        rendered_form = new_form.render(context=context)
        # submit form
        response = client.post(reverse('home:post_events_view'), data=event, mode='same_origin')
        response_json = response.json()
        # check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['valid'], 'false')
        self.assertHTMLEqual(response_json['form'], rendered_form)
        self.assertInHTML(msg, response_json['form'], count=1)

    def test_response_get_fetch_request_post_events_view(self):
        """
        Tests that a GET request for form refreshing, after closing the modal or clicking cancel, receives the expected responses.
        """
        client = Client()
        # existing user sign-in with data
        client.login(email=self.data['email'],
                     password=self.data['password1'])
        # retrieving the original post events modal content
        rendered_post_events_modal = client.get('/home/').context_data['post_events_modal']
        # GET request to reload empty modal form
        response = client.get('/home/post_events/?refresh=true', mode='same_origin')
        response_json = response.json()
        # checking the response status and its json payload
        self.assertEqual(response.status_code, 200)
        self.assertIn('modal', response_json)
        # Check that the prefilled values have been restored. CSRF's are different only.
        self.assertHTMLEqual(re.sub("(<input).+(name=\"csrf).+>", "", rendered_post_events_modal),
                             re.sub("(<input).+(name=\"csrf).+>", "", response_json['modal']))


class TestUpdateEventsView(TestCase):
    """
    Tests for UpdateEventsView.
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

    data3 = {'email': 'tommypaul14789@gmail.com',
             'email2': 'tommypaul14789@gmail.com',
             'password1': 'holly!12345',
             'password2': 'holly!12345',
             'username': 'jimmy14799'}
    
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
        client.post('/accounts/signup/', cls.data3)
        # verify user emails
        user_email = EmailAddress.objects.get(user='tommypaul147@gmail.com')
        user_email.verified = True
        user_email.save()
        user_email2 = EmailAddress.objects.get(user='tommypaul1478@gmail.com')
        user_email2.verified = True
        user_email2.save()
        user_email3 = EmailAddress.objects.get(user='tommypaul14789@gmail.com')
        user_email3.verified = True
        user_email3.save()
        # create profile for user
        cls.user = CustomUserModel.objects.get(email=user_email.email)
        UserProfile.objects.create(user=cls.user,
                                   first_name='jimmy',
                                   last_name='knighton',
                                   date_of_birth='1926-03-25',
                                   sex='male',
                                   bio='I enjoy all outdoor activities.')
        # create address for user
        UserAddress.objects.create(user_profile=cls.user.profile,
                                   address_line_one='57 portland gardens',
                                   city_or_town='chadwell heath',
                                   county='essex',
                                   postcode='rm65uh',
                                   latitude=51.5791,
                                   longitude=0.1355)
        cls.user2 = CustomUserModel.objects.get(username=cls.data2['username'])
        cls.user3 = CustomUserModel.objects.get(username=cls.data3['username'])
        # create events hosted by user.
        EventsActivities.objects.create(host_user=cls.user,
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
        EventsActivities.objects.create(host_user=cls.user,
                                        status="upcoming",
                                        title='event2',
                                        when="2024-10-30 12:00:00",
                                        closing_date="2022-10-15 12:00:00",
                                        max_attendees=20,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1aa')
        # Adding user2 and user3 as attendees of event1 and event2
        EventsActivities.objects.get(title='event1').attendees.add(cls.user2, through_defaults={'status': 'In'})
        EventsActivities.objects.get(title='event1').attendees.add(cls.user3, through_defaults={'status': 'In'})
        EventsActivities.objects.get(title='event2').attendees.add(cls.user2, through_defaults={'status': 'Att'})
        EventsActivities.objects.get(title='event2').attendees.add(cls.user3, through_defaults={'status': 'Att'})

    def test_post_method_of_update_events_view(self):
        """
        Tests the POST method of the UpdateEventsView, that is responsible for handling requests to delete/cancel a host's event advert/upcoming event.
        """
        # Testing delete event request:

        client = Client()
        # user sign-in
        client.login(email=self.data['email'],
                     password=self.data['password1'])
        event_instance = EventsActivities.objects.get(host_user=self.user, title='event1')
        event_id = str(event_instance.id)
        # Make request to delete event
        response = client.post('/home/update_events/?cancel=false', data=event_id, content_type='text/XML')
        # check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'successful': 'true'})
        # check event no longer exists
        self.assertEqual((EventsActivities.objects.filter(id=int(event_id)).exists()), False)
        # check emails have been sent
        event_title = event_instance.title
        event_host = event_instance.host_user.username
        event_when = event_instance.when.strftime("%H:%M, %d/%m/%y")
        subject = f'EventID:{event_id} has been cancelled by the host'
        recipients = [self.data2['email'], self.data3['email']]
        message = f'''Hi,
An event that you have registered your interest in has been cancelled:
Unfortunately the event titled {event_title}, hosted by {event_host}, and due to occur on the {event_when}, has been cancelled.'''
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, subject)
        self.assertEqual(mail.outbox[0].to, recipients)
        self.assertEqual(mail.outbox[0].body, message)
        self.assertEqual(mail.outbox[0].from_email, EMAIL_HOST_USER)

        # Testing cancel event request:

        event_instance = EventsActivities.objects.get(host_user=self.user, title='event2')
        event_id = str(event_instance.id)
        # Make request to cancel event
        response = client.post('/home/update_events/?cancel=true', data=event_id, content_type='text/XML')
        # check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'successful': 'true'})
        # check event no longer exists
        self.assertEqual((EventsActivities.objects.filter(id=int(event_id)).exists()), False)
        # check emails have been sent
        event_title = event_instance.title
        event_host = event_instance.host_user.username
        event_when = event_instance.when.strftime("%H:%M, %d/%m/%y")
        subject = f'EventID:{event_id} has been cancelled by the host'
        recipients = [self.data2['email'], self.data3['email']]
        message = f'''Hi,
One of the events you are confirmed to attend has been cancelled:
Unfortunately the event titled {event_title}, hosted by {event_host}, and due to occur on the {event_when}, has been cancelled.'''
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[1].subject, subject)
        self.assertEqual(mail.outbox[1].to, recipients)
        self.assertEqual(mail.outbox[1].body, message)
        self.assertEqual(mail.outbox[1].from_email, EMAIL_HOST_USER)
    
    def test_post_method_of_update_events_view_with_exception(self):
        """
        Tests the behaviour of the POST method of the UpdateEventsView when an exception occurs related to deleting an event.
        """
        # Testing delete event request:

        client = Client()
        # user sign-in
        client.login(email=self.data['email'],
                     password=self.data['password1'])
        # use non existent invalid event_id to generate a view exception
        event_id = '100'
        # Make request to delete event
        response = client.post('/home/update_events/?cancel=false', data=event_id, content_type='text/XML')
        # check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'successful': 'false'})
        # check event still exists
        self.assertEqual((EventsActivities.objects.filter(host_user=self.user, title='event1')).exists(), True)
        # check emails have not been sent
        self.assertEqual(len(mail.outbox), 0)

        # Testing cancel event request:

        # use non existent invalid event_id to generate a view exception
        event_id = '100'
        # Make request to cancel event
        response = client.post('/home/update_events/?cancel=true', data=event_id, content_type='text/XML')
        # check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'successful': 'false'})
        # check event still exists
        self.assertEqual((EventsActivities.objects.filter(host_user=self.user, title='event2').exists()), True)
        # check emails have not been sent
        self.assertEqual(len(mail.outbox), 0)


class TestViewEventsView(TestCase):
    """
    Tests for ViewEventsView.
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
        Tests that the search and view events section template is rendered as part of an authenticated user's homepage.
        """
        client = Client()
        # sign-in user
        response = client.login(email=self.data['email'],
                                password=self.data['password1'])
        response = client.get('/home/')
        response_code = response.status_code
        self.assertEqual(response_code, 200)
        self.assertTemplateUsed('events_and_activities/search_view_events.html')
    
    def test_response_direct_get_request_post_events_view(self):
        """
        Tests that if a user tries to access the ViewEventsView
        via a GET request to its url, they are redirected.
        """
        # unauthenticated user
        client = Client()
        response = client.get('/home/event_withdrawal/', follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/home/event_withdrawal/')
        # authenticated user
        client.login(email=self.data['email'],
                     password=self.data['password1'])
        response = client.get('/home/event_withdrawal/', follow=True)
        self.assertRedirects(response, '/home/')

    def test_the_search_view_events_section_view_related_logic_and_rendering(self):
        """
        Tests the ViewEventsView GET method for generating the context for the search and view events section template, as well as rendering the template.
        """
        user = CustomUserModel.objects.get(username=self.data['username'])
        user2 = CustomUserModel.objects.get(username=self.data2['username'])
        # create identical events possibly varying in their host, title, status, 'closing date' and or 'when' values.
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
                                        status="upcoming",
                                        title='event2',
                                        when="2024-10-30 12:00:00",
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
                                        closing_date="2028-10-15 12:00:00",
                                        max_attendees=20,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1aa')
        EventsActivities.objects.create(host_user=user2,
                                        status="upcoming",
                                        title='event5',
                                        when="2024-10-30 12:00:00",
                                        closing_date="2022-10-15 12:00:00",
                                        max_attendees=20,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1aa')
        # Adding user as an attendee to event4 and event5
        EventsActivities.objects.get(title='event4').attendees.add(user, through_defaults={'status': 'In'})
        EventsActivities.objects.get(title='event5').attendees.add(user, through_defaults={'status': 'Att'})
        # expected data
        expected_interested_event_data = [({'ID': 4, 'host': user2.username, 'title': 'event4',
                                           'when': "12:00, 23/12/30", 'closing date': "12:00, 15/10/28",
                                           'max no. of attendees': 20, 'keywords': 'outdoors,paintballing,competitive',
                                           'description': 'Paintballing dayout, followed by lunch.',
                                           'requirements': 'min £50 per person. wear suitable shoes. Need to be physically fit.',
                                           'Address line 1': 'mayhem paintball', 'City/Town': 'adbridge',
                                           'County': 'essex', 'Postcode': 'rm4 1aa'}, 1)]
        expected_upcoming_event_data = [({'ID': 5, 'host': user2.username, 'title': 'event5',
                                         'when': "12:00, 30/10/24", 'closing date': "12:00, 15/10/22",
                                         'max no. of attendees': 20, 'keywords': 'outdoors,paintballing,competitive',
                                         'description': 'Paintballing dayout, followed by lunch.',
                                         'requirements': 'min £50 per person. wear suitable shoes. Need to be physically fit.',
                                         'Address line 1': 'mayhem paintball', 'City/Town': 'adbridge',
                                         'County': 'essex', 'Postcode': 'rm4 1aa'}, 1)]
        client = Client()
        client.login(email=self.data['email'],
                     password=self.data['password1'])
        response = client.get('/home/')
        self.assertTemplateUsed(response, 'events_and_activities/search_view_events.html')
        sub_context = {'interested_events_data': expected_interested_event_data,
                       'upcoming_events_data': expected_upcoming_event_data}
        for key, value in sub_context.items():
            with self.subTest(key):
                self.assertEqual(response.context[key], value)
    
    def test_post_method_of_view_events_view(self):
        """
        Tests the POST method of the ViewEventsView, that is responsible for handling requests to withdrawal user from an event.
        """
        user = CustomUserModel.objects.get(username=self.data['username'])
        user2 = CustomUserModel.objects.get(username=self.data2['username'])

        EventsActivities.objects.create(host_user=user2,
                                        status="advertised",
                                        title='event4',
                                        when="2030-12-23 12:00:00",
                                        closing_date="2028-10-15 12:00:00",
                                        max_attendees=20,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1aa')
        EventsActivities.objects.create(host_user=user2,
                                        status="upcoming",
                                        title='event5',
                                        when="2024-10-30 12:00:00",
                                        closing_date="2022-10-15 12:00:00",
                                        max_attendees=20,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1aa')
        # Adding user as an attendee to event4 and event5
        EventsActivities.objects.get(title='event4').attendees.add(user, through_defaults={'status': 'In'})
        EventsActivities.objects.get(title='event5').attendees.add(user, through_defaults={'status': 'Att'})

        client = Client()
        # user sign-in
        client.login(email=self.data['email'],
                     password=self.data['password1'])

        # check user is interested in event4
        self.assertEqual((user.engagement.filter(event__title='event4', status='In')).exists(), True)
        # get the event4 id
        event_instance = EventsActivities.objects.get(title='event4')
        event_id = str(event_instance.id)
        # Make request to withdraw from event4
        response = client.post('/home/event_withdrawal/', data=event_id, content_type='text/XML')
        # check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'successful': 'true'})
        # check user is no longer interested in event4
        self.assertEqual(Engagement.objects.filter(event__title='event4', user=user).exists(), False)
        # check emails have not been sent
        self.assertEqual(len(mail.outbox), 0)

        # check user is attending event5
        self.assertEqual((user.engagement.filter(event__title='event5', status='Att')).exists(), True)
        # get the event5 id
        event_instance = EventsActivities.objects.get(title='event5')
        event_id = str(event_instance.id)
        # Make request to withdraw from event5
        response = client.post('/home/event_withdrawal/', data=event_id, content_type='text/XML')
        # check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'successful': 'true'})
        # check user is no longer attending event5
        self.assertEqual(Engagement.objects.filter(event__title='event5', user=user).exists(), False)
        # check email has been sent
        event_instance = EventsActivities.objects.get(id=int(event_id))
        host_email = event_instance.host_user.email
        event_title = event_instance.title
        event_when = event_instance.when.strftime("%H:%M, %d/%m/%y")
        subject = f'{user.username} has withdrawn from your upcoming event, EventID:{event_id}'
        message = f'''Hi,
{user.username} has withdrawn from one of your upcoming events:
Unfortunately {user.username} has withdrawn from your event titled {event_title}, due to occur on the {event_when}.'''
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, subject)
        self.assertEqual(mail.outbox[0].to, [host_email])
        self.assertEqual(mail.outbox[0].body, message)
        self.assertEqual(mail.outbox[0].from_email, EMAIL_HOST_USER)

    def test_post_method_of_view_events_view_with_exception(self):
        """
        Tests the behaviour of the POST method of the ViewEventsView when an exception occurs.
        """
        user = CustomUserModel.objects.get(username=self.data['username'])
        user2 = CustomUserModel.objects.get(username=self.data2['username'])

        EventsActivities.objects.create(host_user=user2,
                                        status="advertised",
                                        title='event4',
                                        when="2030-12-23 12:00:00",
                                        closing_date="2028-10-15 12:00:00",
                                        max_attendees=20,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1aa')
        EventsActivities.objects.create(host_user=user2,
                                        status="upcoming",
                                        title='event5',
                                        when="2024-10-30 12:00:00",
                                        closing_date="2022-10-15 12:00:00",
                                        max_attendees=20,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1aa')
        # Adding user as an attendee to event4 and event5
        EventsActivities.objects.get(title='event4').attendees.add(user, through_defaults={'status': 'In'})
        EventsActivities.objects.get(title='event5').attendees.add(user, through_defaults={'status': 'Att'})

        client = Client()
        # user sign-in
        client.login(email=self.data['email'],
                     password=self.data['password1'])

        # check user is interested in event4
        self.assertEqual((user.engagement.filter(event__title='event4', status='In')).exists(), True)
        # generate an exception in the view by using a non-existent event_id
        event_id = '100'
        # Make withdrawal request with an invalid event_id
        response = client.post('/home/event_withdrawal/', data=event_id, content_type='text/XML')
        # check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'successful': 'false'})
        # check user is still interested in event4
        self.assertEqual(Engagement.objects.filter(event__title='event4', user=user).exists(), True)
        # check emails have not been sent
        self.assertEqual(len(mail.outbox), 0)
        
        # check user is attending event5
        self.assertEqual((user.engagement.filter(event__title='event5', status='Att')).exists(), True)
        # generate an exception in the view by using a non-existent event_id
        event_id = '100'
        # Make withdrawal request with an invalid event_id
        response = client.post('/home/event_withdrawal/', data=event_id, content_type='text/XML')
        # check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'successful': 'false'})
        # check user is still attending event5
        self.assertEqual(Engagement.objects.filter(event__title='event5', user=user).exists(), True)
        # check emails have not been sent
        self.assertEqual(len(mail.outbox), 0)


class TestSearchAdvertsView(TestCase):
    """
    Tests for SearchAdvertsView.
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

    data3 = {'email': 'tommypaul146@gmail.com',
             'email2': 'tommypaul146@gmail.com',
             'password1': 'holly!157',
             'password2': 'holly!157',
             'username': 'jimmy146'}
    
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
        client.post('/accounts/signup/', cls.data3)
        # verify user emails
        user_email = EmailAddress.objects.get(user='tommypaul147@gmail.com')
        user_email.verified = True
        user_email.save()
        user_email2 = EmailAddress.objects.get(user='tommypaul1478@gmail.com')
        user_email2.verified = True
        user_email2.save()
        user_email3 = EmailAddress.objects.get(user='tommypaul146@gmail.com')
        user_email3.verified = True
        user_email3.save()
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
    
    def test_get_response_existing_authenticated_user(self):
        """
        Tests that the search event adverts page template is rendered for an authenticated user who has already created their profile.
        """
        client = Client()
        # sign-in user
        response = client.login(email=self.data['email'],
                                password=self.data['password1'])
        response = client.get('/events_and_activities/search_event_adverts/')
        response_code = response.status_code
        self.assertEqual(response_code, 200)
        self.assertTemplateUsed(response, 'events_and_activities/search_event_adverts.html')

    def test_get_response_authenticated_user_not_yet_created_profile(self):
        """
        Tests that a new user who has yet to create their profile is redirected to their home page if they try to access the search event adverts page.
        """
        client = Client()
        # sign-in user
        response = client.login(email=self.data2['email'],
                                password=self.data2['password1'])
        response = client.get('/events_and_activities/search_event_adverts/', follow=True)
        response_code = response.status_code
        self.assertEqual(response_code, 200)
        redirect_chain = response.redirect_chain
        self.assertEqual(redirect_chain, [('/home/', 302)])
        self.assertTemplateNotUsed(response, 'events_and_activities/search_event_adverts.html')

    def test_get_response_unauthenticated_user(self):
        """
        Tests that an unauthenticated user is redirected when a GET request is made to the search event adverts page.
        """
        client = Client()
        response = client.get('/events_and_activities/search_event_adverts/', follow=True)
        response_code = response.status_code
        self.assertEqual(response_code, 200)
        redirect_chain = response.redirect_chain
        self.assertEqual(redirect_chain, [('/accounts/login/?next=/events_and_activities/search_event_adverts/', 302)])
        self.assertTemplateUsed(response, 'account/login.html')

    def test_get_method_view_logic_and_advert_retrieval(self):
        """
        Tests that the correct advert instances are retrieved from the EventsActivities Model and rendered, for a user.
        """
        user = CustomUserModel.objects.get(username=self.data['username'])
        user3 = CustomUserModel.objects.get(username=self.data3['username'])
        # create profile for user2
        user2 = CustomUserModel.objects.get(username=self.data2['username'])
        UserProfile.objects.create(user=user2,
                                   first_name='timmy',
                                   last_name='knighton',
                                   date_of_birth='1923-03-25',
                                   sex='male',
                                   bio='I enjoy everything.')
        # create address for user2
        UserAddress.objects.create(user_profile=user2.profile,
                                   address_line_one='58 portland gardens',
                                   city_or_town='chadwell heath',
                                   county='essex',
                                   postcode='rm65uh',
                                   latitude=51.5791,
                                   longitude=0.1355)
        # create event that user2 is interested in already
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
        EventsActivities.objects.get(title='event1').attendees.add(user2, through_defaults={'status': 'In'})
        # create event that user2 is already attending
        EventsActivities.objects.create(host_user=user,
                                        status="confirmed",
                                        title='event2',
                                        when="2028-10-30 12:00:00",
                                        closing_date="2022-10-15 12:00:00",
                                        max_attendees=20,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1aa')
        EventsActivities.objects.get(title='event2').attendees.add(user2, through_defaults={'status': 'Att'})
        # create event that user2 is hosting
        EventsActivities.objects.create(host_user=user2,
                                        status="advertised",
                                        title='event3',
                                        when="2030-12-23 12:00:00",
                                        closing_date="2029-10-15 12:00:00",
                                        max_attendees=20,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1aa')
        # create event that currently has the max number of attendees
        EventsActivities.objects.create(host_user=user,
                                        status="advertised",
                                        title='event4',
                                        when="2030-12-23 12:00:00",
                                        closing_date="2029-10-15 12:00:00",
                                        max_attendees=1,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1aa')
        EventsActivities.objects.get(title='event4').attendees.add(user3, through_defaults={'status': 'In'})
        # create event that should be rendered as an advert for user2
        EventsActivities.objects.create(host_user=user,
                                        status="advertised",
                                        title='event5',
                                        when="2032-10-30 12:00:00",
                                        closing_date="2031-10-15 12:00:00",
                                        max_attendees=20,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1aa')                          
        self.assertEqual(EventsActivities.objects.all().count(), 5)

        client = Client()
        # sign-in user2
        client.login(email=self.data2['email'],
                     password=self.data2['password1'])
        response = client.get('/events_and_activities/search_event_adverts/')
        # expected data
        expected_advert_data = [({'ID': 5, 'host': user.username, 'title': 'event5',
                                  'when': '12:00, 30/10/32', 'closing date': '12:00, 15/10/31',
                                  'max no. of attendees': 20, 'keywords': 'outdoors,paintballing,competitive',
                                  'description': 'Paintballing dayout, followed by lunch.',
                                  'requirements': 'min £50 per person. wear suitable shoes. Need to be physically fit.',
                                  'Address line 1': 'mayhem paintball', 'City/Town': 'adbridge',
                                  'County': 'essex', 'Postcode': 'rm4 1aa'}, 0)]
        self.assertEqual(len(response.context['event_advert_data']), 1)
        self.assertEqual(response.context['event_advert_data'], expected_advert_data)
    
    def test_post_method_response_for_unauthenticated_user(self):
        """
        Tests the response when an unauthenticated user tries to register their interest in an event
        """
        user = CustomUserModel.objects.get(username=self.data['username'])
        user2 = CustomUserModel.objects.get(username=self.data2['username'])
    
        # create event1
        EventsActivities.objects.create(host_user=user,
                                        status="advertised",
                                        title='event1',
                                        when="2032-10-30 12:00:00",
                                        closing_date="2031-10-15 12:00:00",
                                        max_attendees=20,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1aa')
        client = Client()
        # get the event1 id
        event_instance = EventsActivities.objects.get(title='event1')
        event_id = str(event_instance.id)
        # Make post request to register interest in event1
        response = client.post('/events_and_activities/search_event_adverts/', data=event_id, content_type='text/XML', follow=True)
        # check response
        self.assertEqual(response.status_code, 200)
        redirect_chain = response.redirect_chain
        self.assertEqual(redirect_chain, [('/accounts/login/?next=/events_and_activities/search_event_adverts/', 302)])
        self.assertTemplateUsed(response, 'account/login.html')

    def test_post_method_for_successful_request(self):
        """
        Tests the method code for when the criteria are met for a successful request to register a user's interest in an event.
        """
        user = CustomUserModel.objects.get(username=self.data['username'])
        user2 = CustomUserModel.objects.get(username=self.data2['username'])
        user3 = CustomUserModel.objects.get(username=self.data3['username'])
        # create event that user2 is interested in already
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
        EventsActivities.objects.get(title='event1').attendees.add(user2, through_defaults={'status': 'In'})
        # create event that user2 is already attending
        EventsActivities.objects.create(host_user=user,
                                        status="confirmed",
                                        title='event2',
                                        when="2028-10-30 12:00:00",
                                        closing_date="2022-10-15 12:00:00",
                                        max_attendees=20,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1aa')
        EventsActivities.objects.get(title='event2').attendees.add(user2, through_defaults={'status': 'Att'})
        # create event that user2 is hosting
        EventsActivities.objects.create(host_user=user2,
                                        status="advertised",
                                        title='event3',
                                        when="2030-12-23 12:00:00",
                                        closing_date="2029-10-15 12:00:00",
                                        max_attendees=20,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1aa')
        # create event that currently has the max number of attendees
        EventsActivities.objects.create(host_user=user,
                                        status="advertised",
                                        title='event4',
                                        when="2030-12-23 12:00:00",
                                        closing_date="2029-10-15 12:00:00",
                                        max_attendees=1,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1aa')
        EventsActivities.objects.get(title='event4').attendees.add(user3, through_defaults={'status': 'In'})
        # create event that should be rendered as an advert for user2
        EventsActivities.objects.create(host_user=user,
                                        status="advertised",
                                        title='event5',
                                        when="2032-10-30 12:00:00",
                                        closing_date="2031-10-15 12:00:00",
                                        max_attendees=20,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1aa')
        client = Client()
        # sign-in user2
        client.login(email=self.data2['email'],
                     password=self.data2['password1'])
        response = client.get('/events_and_activities/search_event_adverts/')
        # get the event5 id
        event_instance = EventsActivities.objects.get(title='event5')
        event_id = str(event_instance.id)
        # Make post request to register interest in event5
        response = client.post('/events_and_activities/search_event_adverts/', data=event_id, content_type='text/XML')
        # check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'successful': 'true'})
        # check user2 is interested in event5
        self.assertTrue(event_instance.engagement.filter(user=user2, status='In').exists())

    def test_post_method_for_unsuccessful_request_due_to_hosting_event_clash(self):
        """
        Tests the response when a user attempts to register interest in an event that occurs on the same date as an event they are hosting.
        """
        user = CustomUserModel.objects.get(username=self.data['username'])
        user2 = CustomUserModel.objects.get(username=self.data2['username'])
        user3 = CustomUserModel.objects.get(username=self.data3['username'])
        # create event that user2 is hosting
        EventsActivities.objects.create(host_user=user2,
                                        status="advertised",
                                        title='event1',
                                        when="2032-10-30 12:00:00",
                                        closing_date="2029-10-15 12:00:00",
                                        max_attendees=20,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1aa')
        # create event on the same date as event1 
        EventsActivities.objects.create(host_user=user,
                                        status="advertised",
                                        title='event2',
                                        when="2032-10-30 12:00:00",
                                        closing_date="2031-10-15 12:00:00",
                                        max_attendees=20,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1aa')
        client = Client()
        # sign-in user2
        client.login(email=self.data2['email'],
                     password=self.data2['password1'])
        response = client.get('/events_and_activities/search_event_adverts/')
        # get the event2 id
        event_instance = EventsActivities.objects.get(title='event2')
        event_id = str(event_instance.id)
        # Make post request to register interest in event2
        response = client.post('/events_and_activities/search_event_adverts/', data=event_id, content_type='text/XML')
        # check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'successful': 'false', 'error_msg': EventClash('event1', '1', host=True).msg, 'error_type': 'clash'})
        # check user2 is not interested in event2
        self.assertFalse(event_instance.engagement.filter(user=user2, status='In').exists())

    def test_post_method_for_unsuccessful_request_due_to_engaged_event_clash(self):
        """
        Tests the response when a user attempts to register interest in an event that occurs on the same date as an event they are interested in or are attending.
        """
        user = CustomUserModel.objects.get(username=self.data['username'])
        user2 = CustomUserModel.objects.get(username=self.data2['username'])
        user3 = CustomUserModel.objects.get(username=self.data3['username'])
        # create event that user2 is interested in already
        EventsActivities.objects.create(host_user=user,
                                        status="advertised",
                                        title='event1',
                                        when="2032-10-30 11:00:00",
                                        closing_date="2028-12-15 12:00:00",
                                        max_attendees=20,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1aa')
        EventsActivities.objects.get(title='event1').attendees.add(user2, through_defaults={'status': 'In'})
        # create event that user2 is already attending
        EventsActivities.objects.create(host_user=user,
                                        status="confirmed",
                                        title='event2',
                                        when="2033-10-30 13:00:00",
                                        closing_date="2022-10-15 12:00:00",
                                        max_attendees=20,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1aa')
        EventsActivities.objects.get(title='event2').attendees.add(user2, through_defaults={'status': 'Att'})
        # create event on the same date as event1 
        EventsActivities.objects.create(host_user=user,
                                        status="advertised",
                                        title='event3',
                                        when="2032-10-30 9:00:00",
                                        closing_date="2031-10-15 12:00:00",
                                        max_attendees=20,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1aa')
        # create event on the same date as event2 
        EventsActivities.objects.create(host_user=user,
                                        status="advertised",
                                        title='event4',
                                        when="2033-10-30 14:00:00",
                                        closing_date="2031-10-15 12:00:00",
                                        max_attendees=20,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1aa')
        client = Client()
        # sign-in user2
        client.login(email=self.data2['email'],
                     password=self.data2['password1'])
        response = client.get('/events_and_activities/search_event_adverts/')
        # get the event3 id
        event_instance = EventsActivities.objects.get(title='event3')
        event_id = str(event_instance.id)
        # Make post request to register interest in event3
        response = client.post('/events_and_activities/search_event_adverts/', data=event_id, content_type='text/XML')
        # check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'successful': 'false', 'error_msg': EventClash('event1', '1', interested=True).msg, 'error_type': 'clash'})
        # check user2 is not interested in event3
        self.assertFalse(event_instance.engagement.filter(user=user2, status='In').exists())

        # get the event4 id
        event_instance = EventsActivities.objects.get(title='event4')
        event_id = str(event_instance.id)
        # Make post request to register interest in event4
        response = client.post('/events_and_activities/search_event_adverts/', data=event_id, content_type='text/XML')
        # check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'successful': 'false', 'error_msg': EventClash('event2', '2', attending=True).msg, 'error_type': 'clash'})
        # check user2 is not interested in event4
        self.assertFalse(event_instance.engagement.filter(user=user2, status='In').exists())


    def test_post_method_for_unsuccessful_request_due_to_max_attendees(self):
        """
        Tests the response when a user attempts to register interest in an event that just now achieved its maximum number of attendees.
        """
        user = CustomUserModel.objects.get(username=self.data['username'])
        user2 = CustomUserModel.objects.get(username=self.data2['username'])
        user3 = CustomUserModel.objects.get(username=self.data3['username'])
        # create event that currently has the max number of attendees
        EventsActivities.objects.create(host_user=user,
                                        status="advertised",
                                        title='event1',
                                        when="2030-12-23 12:00:00",
                                        closing_date="2029-10-15 12:00:00",
                                        max_attendees=1,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1aa')
        EventsActivities.objects.get(title='event1').attendees.add(user3, through_defaults={'status': 'In'})
        client = Client()
        # sign-in user2
        client.login(email=self.data2['email'],
                     password=self.data2['password1'])
        response = client.get('/events_and_activities/search_event_adverts/')
        # get the event1 id
        event_instance = EventsActivities.objects.get(title='event1')
        event_id = str(event_instance.id)
        # Make post request to register interest in event1
        response = client.post('/events_and_activities/search_event_adverts/', data=event_id, content_type='text/XML')
        # check response
        self.assertEqual(response.status_code, 200)
        msg = 'Interest not registered. Sorry but the maximum number of people for this event have just now registered their interest.'
        self.assertEqual(response.json(), {'successful': 'false', 'error_msg': msg, 'error_type': 'max_people'})
        # check user2 is not interested in event1
        self.assertFalse(event_instance.engagement.filter(user=user2, status='In').exists())

    def test_post_method_for_unsuccessful_request_due_to_other_exception(self):
        """
        Tests the response when an exception occurs related to the database or similar, when a user attempts to register interest in an event.
        """
        user = CustomUserModel.objects.get(username=self.data['username'])
        user2 = CustomUserModel.objects.get(username=self.data2['username'])
        # create event
        EventsActivities.objects.create(host_user=user,
                                        status="advertised",
                                        title='event1',
                                        when="2030-12-23 12:00:00",
                                        closing_date="2029-10-15 12:00:00",
                                        max_attendees=1,
                                        keywords="outdoors,paintballing,competitive",
                                        description="Paintballing dayout, followed by lunch.",
                                        requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                        address_line_one='mayhem paintball',
                                        city_or_town='adbridge',
                                        county='essex',
                                        postcode='rm4 1aa')
        client = Client()
        # sign-in user2
        client.login(email=self.data2['email'],
                     password=self.data2['password1'])
        response = client.get('/events_and_activities/search_event_adverts/')
        # give an invalid event_id to simulate an exception
        event_id = str('5')
        # Make post request to register interest in event1
        response = client.post('/events_and_activities/search_event_adverts/', data=event_id, content_type='text/XML')
        # check response
        self.assertEqual(response.status_code, 200)
        msg = '''Unable to register your interest in this event at this time. Please refresh the page and try again. If the problem
persists, please contact us.''' 
        self.assertEqual(response.json(), {'successful': 'false', 'error_msg': msg, 'error_type': 'database'})
        # check user2 is not interested in event1
        self.assertFalse(EventsActivities.objects.get(id='1').engagement.filter(user=user2, status='In').exists())


class TestRetrieveAttendeeContactInfoView(TestCase):
    """
    Tests for theRetrieveAttendeeContactInfoView.
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

    data3 = {'email': 'tommypaul146@gmail.com',
             'email2': 'tommypaul146@gmail.com',
             'password1': 'holly!157',
             'password2': 'holly!157',
             'username': 'jimmy146'}
    
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
        client.post('/accounts/signup/', cls.data3)
        # verify user emails
        user_email = EmailAddress.objects.get(user='tommypaul147@gmail.com')
        user_email.verified = True
        user_email.save()
        user_email2 = EmailAddress.objects.get(user='tommypaul1478@gmail.com')
        user_email2.verified = True
        user_email2.save()
        user_email3 = EmailAddress.objects.get(user='tommypaul146@gmail.com')
        user_email3.verified = True
        user_email3.save()
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
    
    def test_post_method_response_for_unauthenticated_user(self):
        """
        Tests the response when an unauthenticated user makes a POST request.
        """
        user = CustomUserModel.objects.get(username=self.data['username'])
        user2 = CustomUserModel.objects.get(username=self.data2['username'])
    
        # create event1
        event1 = EventsActivities.objects.create(host_user=user,
                                                 status="confirmed",
                                                 title='event1',
                                                 when="2032-10-30 12:00:00",
                                                 closing_date="2022-10-15 12:00:00",
                                                 max_attendees=20,
                                                 keywords="outdoors,paintballing,competitive",
                                                 description="Paintballing dayout, followed by lunch.",
                                                 requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                                 address_line_one='mayhem paintball',
                                                 city_or_town='adbridge',
                                                 county='essex',
                                                 postcode='rm4 1aa')
        event1.attendees.add(user2, through_defaults={'status': 'Att'})
        client = Client()
        # get the event1 id
        event_id = str(event1.id)
        # set host parameter
        host = 'no'
        # Make post request
        response = (client.
                    post(reverse('events_and_activities:retrieve_contact_info'), data=json.dumps({'event_id': event_id,'host': host}), content_type='application/json', follow=True))
        # check response
        self.assertEqual(response.status_code, 200)
        redirect_chain = response.redirect_chain
        self.assertEqual(redirect_chain, [('/accounts/login/?next=/events_and_activities/retrieve_contact_info/', 302)])
        self.assertTemplateUsed(response, 'account/login.html')

    def test_post_method_for_successful_request_for_attendee_info(self):
        """
        Tests the POST method for a successful request for attendee contact info.
        """
        user = CustomUserModel.objects.get(username=self.data['username'])
        user2 = CustomUserModel.objects.get(username=self.data2['username'])
        user3 = CustomUserModel.objects.get(username=self.data3['username'])
        # create event that user1 is confirmed to host
        event1 = EventsActivities.objects.create(host_user=user,
                                                 status="confirmed",
                                                 title='event1',
                                                 when="2030-12-23 12:00:00",
                                                 closing_date="2022-12-15 12:00:00",
                                                 max_attendees=20,
                                                 keywords="outdoors,paintballing,competitive",
                                                 description="Paintballing dayout, followed by lunch.",
                                                 requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                                 address_line_one='mayhem paintball',
                                                 city_or_town='adbridge',
                                                 county='essex',
                                                 postcode='rm4 1aa')
        # add user2 and user3 as confirmed attendees
        event1.attendees.add(user2, through_defaults={'status': 'Att'})
        event1.attendees.add(user3, through_defaults={'status': 'Att'})
        client = Client()
        # sign-in user
        client.login(email=self.data['email'],
                     password=self.data['password1'])
        # get the event1 id
        event_id = str(event1.id)
        # set host parameter
        host = 'no'
        # Make post request
        response = client.post(reverse('events_and_activities:retrieve_contact_info'), data=json.dumps({'event_id': event_id,'host': host}), content_type='application/json')
        # check response
        self.assertEqual(response.status_code, 200)
        context = {'contact_info': [(user2.username, user2.email), (user3.username, user3.email)], 'modal': 'attendee_contact_info', 'button1_name': 'close',
                   'event_id': '1', 'event_title': 'event1'}
        rendered_modal = render_to_string(request=response.request, context=context, template_name='events_and_activities/contact_info_modal.html')
        self.assertEqual(response.json(), {'successful': 'true', 'rendered_modal': rendered_modal[rendered_modal.index('<div id="attendee_contact_info" class="modal"'):-6]})

    def test_post_method_for_successful_request_for_host_info(self):
        """
        Tests the POST method for a successful request for host contact info.
        """
        user = CustomUserModel.objects.get(username=self.data['username'])
        user2 = CustomUserModel.objects.get(username=self.data2['username'])
        user3 = CustomUserModel.objects.get(username=self.data3['username'])
        # create event that user1 is confirmed to host
        event1 = EventsActivities.objects.create(host_user=user,
                                                 status="confirmed",
                                                 title='event1',
                                                 when="2030-12-23 12:00:00",
                                                 closing_date="2022-12-15 12:00:00",
                                                 max_attendees=20,
                                                 keywords="outdoors,paintballing,competitive",
                                                 description="Paintballing dayout, followed by lunch.",
                                                 requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                                 address_line_one='mayhem paintball',
                                                 city_or_town='adbridge',
                                                 county='essex',
                                                 postcode='rm4 1aa')
        # add user2 and user3 as confirmed attendees
        event1.attendees.add(user2, through_defaults={'status': 'Att'})
        event1.attendees.add(user3, through_defaults={'status': 'Att'})
        client = Client()
        # sign-in user2
        client.login(email=self.data2['email'],
                     password=self.data2['password1'])
        # get the event1 id
        event_id = str(event1.id)
        # set host parameter
        host = 'yes'
        # Make post request
        response = client.post(reverse('events_and_activities:retrieve_contact_info'), data=json.dumps({'event_id': event_id,'host': host}), content_type='application/json')
        # check response
        self.assertEqual(response.status_code, 200)
        context = {'contact_info': [(user.username, user.email)], 'modal': 'host_contact_info', 'button1_name': 'close',
                   'event_id': '1', 'event_title': 'event1'}
        rendered_modal = render_to_string(request=response.request, context=context, template_name='events_and_activities/contact_info_modal.html')
        self.assertEqual(response.json(), {'successful': 'true', 'rendered_modal': rendered_modal[rendered_modal.index('<div id="host_contact_info" class="modal"'):-6]})


    def test_post_method_for_unsuccessful_request_for_attendee_info_due_to_exception(self):
        """
        Tests exception handling of POST method for request for attendee contact info, and the consequent response.
        """
        user = CustomUserModel.objects.get(username=self.data['username'])
        user2 = CustomUserModel.objects.get(username=self.data2['username'])
        user3 = CustomUserModel.objects.get(username=self.data3['username'])
        # create event that user1 is confirmed to host
        event1 = EventsActivities.objects.create(host_user=user,
                                                 status="confirmed",
                                                 title='event1',
                                                 when="2030-12-23 12:00:00",
                                                 closing_date="2022-12-15 12:00:00",
                                                 max_attendees=20,
                                                 keywords="outdoors,paintballing,competitive",
                                                 description="Paintballing dayout, followed by lunch.",
                                                 requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                                 address_line_one='mayhem paintball',
                                                 city_or_town='adbridge',
                                                 county='essex',
                                                 postcode='rm4 1aa')
        # add user2 and user3 as confirmed attendees
        event1.attendees.add(user2, through_defaults={'status': 'Att'})
        event1.attendees.add(user3, through_defaults={'status': 'Att'})
        client = Client()
        # sign-in user
        client.login(email=self.data['email'],
                     password=self.data['password1'])
        # Simulate database exception by using invalid event id
        event_id = '10'
        # set host parameter
        host = 'no'
        # Make post request
        response = client.post(reverse('events_and_activities:retrieve_contact_info'), data=json.dumps({'event_id': event_id,'host': host}), content_type='application/json')
        # check response
        self.assertEqual(response.status_code, 200)
        msg = '''Unable to retrieve the contact information of the attendees of this event at this time. Please refresh the page and try again. If the problem
persists, please contact us.''' 
        self.assertEqual(response.json(), {'successful': 'false', 'error_msg': msg})
    
    def test_post_method_for_unsuccessful_request_for_host_info_due_to_exception(self):
        """
        Tests exception handling of POST method for request for host contact info, and the consequent response.
        """
        user = CustomUserModel.objects.get(username=self.data['username'])
        user2 = CustomUserModel.objects.get(username=self.data2['username'])
        user3 = CustomUserModel.objects.get(username=self.data3['username'])
        # create event that user1 is confirmed to host
        event1 = EventsActivities.objects.create(host_user=user,
                                                 status="confirmed",
                                                 title='event1',
                                                 when="2030-12-23 12:00:00",
                                                 closing_date="2022-12-15 12:00:00",
                                                 max_attendees=20,
                                                 keywords="outdoors,paintballing,competitive",
                                                 description="Paintballing dayout, followed by lunch.",
                                                 requirements="min £50 per person. wear suitable shoes. Need to be physically fit.",
                                                 address_line_one='mayhem paintball',
                                                 city_or_town='adbridge',
                                                 county='essex',
                                                 postcode='rm4 1aa')
        # add user2 and user3 as confirmed attendees
        event1.attendees.add(user2, through_defaults={'status': 'Att'})
        event1.attendees.add(user3, through_defaults={'status': 'Att'})
        client = Client()
        # sign-in user2
        client.login(email=self.data2['email'],
                     password=self.data2['password1'])
        # Simulate database exception by using invalid event id
        event_id = '10'
        # set host parameter
        host = 'yes'
        # Make post request
        response = client.post(reverse('events_and_activities:retrieve_contact_info'), data=json.dumps({'event_id': event_id,'host': host}), content_type='application/json')
        # check response
        self.assertEqual(response.status_code, 200)
        msg = '''Unable to retrieve the contact information of the host of this event at this time. Please refresh the page and try again. If the problem
persists, please contact us.''' 
        self.assertEqual(response.json(), {'successful': 'false', 'error_msg': msg})