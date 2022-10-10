from django.test import TestCase
from django.test import Client
from allauth.account.models import EmailAddress

# Create your tests here.


class TestViews(TestCase):
    """
    Tests for all views.
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
        
    def test_landing_page_response_anonymous_user(self):
        """
        Tests status code for landing page get request by an anonymous user.
        """
        client = Client()
        response_code = client.get('').status_code
        self.assertEqual(response_code, 200)

    def test_landing_page_rendered_template_anonymous_user(self):
        """
        Tests the correct template is rendered for a landing page url
        get request by an anonymous user.
        """
        client = Client()
        response = client.get('')
        self.assertTemplateUsed(response, 'landing_page/landing_page.html')
        self.assertEqual(response.context['slogan'],
                         'Events & Activities Organised by You for You')
        self.assertEqual(response.context['page_id'], 'landing_page')

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

    def test_landing_page_rendered_template_authenticated_user(self):
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
        self.assertEqual(response.context['logged_in'],
                         True)
        self.assertEqual(response.context['page_id'], 'home_page')
