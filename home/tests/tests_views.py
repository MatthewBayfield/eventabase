from django.test import TestCase
from django.test import Client
from allauth.account.models import EmailAddress

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
        user = EmailAddress.objects.get(user='tommypaul147@gmail.com')
        user.verified = True
        user.save()
        
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

    def test_home_page_response_rendered_template_authenticated_user(self):
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
