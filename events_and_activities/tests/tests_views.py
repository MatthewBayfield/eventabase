from django.test import TestCase
from django.test import Client
from django.urls import reverse
from allauth.account.models import EmailAddress
from landing_page.models import CustomUserModel
from home.models import UserAddress, UserProfile


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

    



