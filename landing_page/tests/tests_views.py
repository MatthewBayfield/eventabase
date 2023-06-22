from django.test import TestCase
from django.test import Client
from allauth.account.models import EmailAddress

# Create your tests here.


class TestLandingPageView(TestCase):
    """
    Tests for LandingPage view.
    """
    data = {'email': 'tommypaul147@gmail.com',
            'email2': 'tommypaul147@gmail.com',
            'password1': 'holly!123',
            'password2': 'holly!123',
            'username': 'jimmy147'}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Sign-up new user 
        client = Client()
        client.post('/accounts/signup/', cls.data)
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
        self.assertEqual(response.context['logged_in'],
                         True)
        self.assertEqual(response.context['page_id'], 'home_page')


class TestTermsPoliciesView(TestCase):
    """
    Tests for the TermsPoliciesView.
    """
    data = {'email': 'tommypaul147@gmail.com',
            'email2': 'tommypaul147@gmail.com',
            'password1': 'holly!123',
            'password2': 'holly!123',
            'username': 'jimmy147'}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Sign-up new user 
        client = Client()
        client.post('/accounts/signup/', cls.data)
        # verify user email
        user = EmailAddress.objects.get(user='tommypaul147@gmail.com')
        user.verified = True
        user.save()

    def test_get_request_logged_in_user(self):
        """
        Test response for get request from logged-in user.
        """
        client = Client()
        # sign-in user
        response = client.login(email=self.data['email'],
                                password=self.data['password1'])
        self.assertTrue(response)
        # get request to terms and conditions page
        response = client.get('/terms_and_policies/', follow=True)
        response_code = response.status_code
        self.assertEqual(response_code, 200)
        self.assertTemplateUsed(response, "landing_page/terms_and_conditions.html")
        self.assertIn('logged_in', response.context.keys())
        self.assertTrue(response.context['logged_in'])
    
    def test_get_request_unauthenticated_user(self):
        """
        Test response for get request from unauthenticated user.
        """
        client = Client()
        # get request to terms and conditions page
        response = client.get('/terms_and_policies/', follow=True)
        response_code = response.status_code
        self.assertEqual(response_code, 200)
        self.assertTemplateUsed(response, "landing_page/terms_and_conditions.html")
        self.assertIn('logged_in', response.context.keys())
        self.assertFalse(response.context['logged_in'])
