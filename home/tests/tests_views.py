from django.test import TestCase
from django.test import Client
from allauth.account.models import EmailAddress
from landing_page.models import CustomUserModel
from home.models import UserAddress, UserProfile
import datetime

# Create your tests here.


class TestHomeViews(TestCase):
    """
    Tests for all home views.
    """
    data = {'email': 'tommypaul147@gmail.com',
            'email2': 'tommypaul147@gmail.com',
            'password1': 'holly!123',
            'password2': 'holly!123',
            'username': 'jimmy147'}

    def setUp(self):
        # Sign-up new user 
        client = Client()
        client.post('/accounts/signup/', self.data)
        # verify user email
        user_email = EmailAddress.objects.get(user='tommypaul147@gmail.com')
        user_email.verified = True
        user_email.save()
        # create profile for user
        user = CustomUserModel.objects.get(email=user_email.email)
        UserProfile.objects.create(username=user,
                                   first_name='jimmy',
                                   last_name='knighton',
                                   date_of_birth='1926-03-25',
                                   sex='male',
                                   bio='I enjoy all outdoor activities.')
        # create address for user
        UserAddress.objects.create(username=user.profile,
                                   address_line_one='57 portland gardens',
                                   city_or_town='chadwell heath',
                                   county='essex',
                                   postcode='rm65uh',
                                   latitude=51.5791,
                                   longitude=0.1355)

    def test_home_page_response_anonymous_user(self):
        """
        Tests status code for home page get request by an anonymous user.
        """
        client = Client()
        response = client.get('/home/', follow=True)
        response_code = response.status_code
        redirect_chain = response.redirect_chain
        self.assertEqual(response_code, 200)
        self.assertEqual(redirect_chain, [('/accounts/login/?next=/home/', 302)])

    def test_home_page_response_rendered_template_anonymous_user(self):
        """
        Tests the correct template is rendered for a home page url
        get request by an anonymous user.
        """
        client = Client()
        response = client.get('/home/', follow=True)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_home_page_response_authenticated_user(self):
        """
        Tests status code for home page get request by an authenticated user.
        """
        client = Client()
        # sign-in user
        response = client.login(email=self.data['email'],
                                password=self.data['password1'])
        self.assertTrue(response)
        response = client.get('/home/')
        response_code = response.status_code
        self.assertEqual(response_code, 200)

    def test_home_page_response_rendered_template_authenticated_user(self):
        """
        Tests the correct template is rendered for a home page url
        get request by an authenticated user.
        """
        client = Client()
        # sign-in user
        response = client.login(email=self.data['email'],
                                password=self.data['password1'])
        self.assertTrue(response)
        response = client.get('/home/')
        self.assertTemplateUsed(response, 'home/home.html')
        sub_context = {'page_id': 'home_page',
                       'logged_in': True,
                       'username': self.data['username']}
        for key, value in sub_context.items():
            with self.subTest(key):
                self.assertEqual(response.context[key], value)

    def test_landing_page_response_authenticated_user(self):
        """
        Tests status code for landing page get request by an authenticated user.
        """
        client = Client()
        # sign-in user
        response = client.login(email=self.data['email'],
                                password=self.data['password1'])
        self.assertTrue(response)
        # get request to landing page url
        response = client.get('', follow=True)
        response_code = response.status_code
        redirect_chain = response.redirect_chain
        self.assertEqual(response_code, 200)
        self.assertEqual(redirect_chain, [('/home/', 302)])

    def test_landing_page_response_rendered_template_authenticated_user(self):
        """
        Tests the correct template is rendered for a landing page url
        get request by an authenticated user.
        """
        client = Client()
        # sign-in user
        response = client.login(email=self.data['email'],
                                password=self.data['password1'])
        self.assertTrue(response)
        # get request to landing page url
        response = client.get('', follow=True)
        self.assertTemplateUsed(response, 'home/home.html')
        sub_context = {'page_id': 'home_page',
                       'logged_in': True,
                       'username': self.data['username']}
        for key, value in sub_context.items():
            with self.subTest(key):
                self.assertEqual(response.context[key], value)
    
    # # will add in the near future
    # def test_authenticated_staff_user_home_page_response(self):
    #     """
    #     """

    def test_profile_template_rendering(self):
        """
        """
        client = Client()
        # sign-in user
        client.login(email=self.data['email'],
                     password=self.data['password1'])
        response = client.get('/home/')
        self.assertTemplateUsed(response, 'home/profile.html')
        expected_user_profile_data = {'first name': 'jimmy',
                                      'last name': 'knighton',
                                      'date of birth': datetime.date(1926, 3, 25),
                                      'sex': 'male', 'bio': 'I enjoy all outdoor activities.'}.items()
        expected_user_address_data = {'Address line 1': '57 portland gardens',
                                      'City/Town': 'chadwell heath',
                                      'County': 'essex',
                                      'Postcode': 'rm65uh'}.items()

        sub_context = {'user_profile_data': expected_user_profile_data,
                       'user_address_data': expected_user_address_data}
        for key, value in sub_context.items():
            with self.subTest(key):
                self.assertEqual(response.context[key], value)
