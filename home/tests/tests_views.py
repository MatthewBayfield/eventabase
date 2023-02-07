import re
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from allauth.account.models import EmailAddress
from landing_page.models import CustomUserModel
from ..models import UserAddress, UserProfile
from ..forms import EditAddress, EditPersonalInfo


# Create your tests here.


class TestHomeViews(TestCase):
    """
    Tests for all home app views.
    """
    maxDiff = None
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

    def test_profile_template_rendering_not_first_login(self):
        """
        Tests the view logic and that the profile template is rendered with the correct context
        for a user, for who it is not their first login.
        """
        client = Client()
        # sign-in user (not first login)
        client.login(email=self.data['email'],
                     password=self.data['password1'])
        response = client.get('/home/')
        self.assertTemplateUsed(response, 'home/profile.html')
        self.assertContains(response, response.context['profile'], html=True)
        expected_user_profile_data = {'first name': 'jimmy',
                                      'last name': 'knighton',
                                      'date of birth': '25/03/1926',
                                      'sex': 'male', 'bio': 'I enjoy all outdoor activities.'}.items()
        expected_user_address_data = {'Address line 1': '57 portland gardens',
                                      'City/Town': 'chadwell heath',
                                      'County': 'essex',
                                      'Postcode': 'rm65uh'}.items()

        sub_context = {'first_login': False,
                       'user_profile_data': expected_user_profile_data,
                       'user_address_data': expected_user_address_data,
                       'button1_name': 'Done',
                       'button2_name': 'Cancel'}
        for key, value in sub_context.items():
            with self.subTest(msg=key):
                self.assertEqual(response.context[key], value)
    
    def test_profile_template_rendering_first_login(self):
        """
        Tests the view logic and that the profile template is rendered with the correct context
        for a user, for who it is their first login.
        """
        client = Client()
        # sign-in user (first login)
        client.login(email=self.data2['email'],
                     password=self.data2['password1'])
        response = client.get('/home/')
        self.assertTemplateUsed(response, 'home/profile.html')
        self.assertContains(response, response.context['profile'], html=True)
        expected_user_profile_data = {'first name': '',
                                      'last name': '',
                                      'date of birth': '',
                                      'sex': '', 'bio': ''}.items()
        expected_user_address_data = {'Address line 1': '',
                                      'City/Town': '',
                                      'County': '',
                                      'Postcode': ''}.items()

        sub_context = {'first_login': True,
                       'user_profile_data': expected_user_profile_data,
                       'user_address_data': expected_user_address_data,
                       'button1_name': 'Done',
                       'button2_name': 'Cancel'}
        for key, value in sub_context.items():
            with self.subTest(key):
                self.assertEqual(response.context[key], value)

    def test_edit_profile_modal_template_rendering_not_first_login(self):
        """
        Tests the view logic and that the edit profile modal template is rendered with the correct context
        for a user, for who it is not their first login.
        """
        client = Client()
        # sign-in user (not first login)
        client.login(email=self.data['email'],
                     password=self.data['password1'])
        response = client.get('/home/')
        self.assertTemplateUsed(response, 'base_modal.html')
        self.assertTemplateUsed(response, 'home/edit_profile_modal.html')
        self.assertContains(response, response.context['edit_profile_modal'], html=True)

        sub_context = {'first_login': False}
        for key, value in sub_context.items():
            with self.subTest(key):
                self.assertEqual(response.context[key], value)

    def test_edit_profile_modal_template_rendering_first_login(self):
        """
        Tests the view logic and that the edit profile modal template is rendered with the correct context
        for a user, for who it is their first login.
        """
        client = Client()
        # sign-in user (first login)
        client.login(email=self.data2['email'],
                     password=self.data2['password1'])
        response = client.get('/home/')
        self.assertTemplateUsed(response, 'base_modal.html')
        self.assertTemplateUsed(response, 'home/edit_profile_modal.html')
        self.assertContains(response, response.context['edit_profile_modal'], html=True)

        sub_context = {'first_login': True}
        for key, value in sub_context.items():
            with self.subTest(key):
                self.assertEqual(response.context[key], value)

    def test_edit_profile_form_template_rendering_not_first_login(self):
        """
        Tests the view logic and that the edit profile form template is rendered with the correct context
        for a user, for who it is not their first login (has profile).
        """
        client = Client()
        # sign-in user (not first login)
        client.login(email=self.data['email'],
                     password=self.data['password1'])
        response = client.get('/home/')
        # checking the personal_info_form context variable
        user = response.context['user']
        user_profile = user.profile
        user_personal_info_data = user_profile.retrieve_field_data(False)
        user_personal_info_data['date_of_birth'] = user_personal_info_data['date_of_birth'].strftime('%d/%m/%Y')
        form = EditPersonalInfo(initial=user_personal_info_data)
        self.assertHTMLEqual(str(response.context['personal_info_form']), str(form))
        # checking the address_form context variable
        user_address = user_profile.address
        user_address_data = user_address.retrieve_field_data(False)
        form = EditAddress(initial=user_address_data)
        self.assertHTMLEqual(str(response.context['address_form']), str(form))

        sub_context = {'first_login': False}
        for key, value in sub_context.items():
            with self.subTest(key):
                self.assertEqual(response.context[key], value)

    def test_edit_profile_form_template_rendering_first_login(self):
        """
        Tests the view logic and that the edit profile form template is rendered with the correct context
        for a user, for who it is their first login (has no profile).
        """
        client = Client()
        # sign-in user (first login)
        client.login(email=self.data2['email'],
                     password=self.data2['password1'])
        response = client.get('/home/')
        # checking the personal_info_form context variable
        form = EditPersonalInfo()
        self.assertHTMLEqual(str(response.context['personal_info_form']), str(form))
        # checking the address_form context variable
        form = EditAddress()
        self.assertHTMLEqual(str(response.context['address_form']), str(form))

        sub_context = {'first_login': True}
        for key, value in sub_context.items():
            with self.subTest(key):
                self.assertEqual(response.context[key], value)

    def test_response_external_get_request_profile_form_view(self):
        """
        Tests that if a user tries to access the ProfileFormView
        via a GET request to its url, they are redirected.
        """
        # unauthenticated user
        client = Client()
        response = client.get('/home/profile_form/', follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/home/profile_form/')
        # authenticated user
        client.login(email=self.data['email'],
                     password=self.data['password1'])
        response = client.get('/home/profile_form/', follow=True)
        self.assertRedirects(response, '/home/')

    def test_response_post_request_profile_form_view_invalid_forms_new_user(self):
        """
        Tests that a post request with invalid form data, and using a new user, receives the expected responses.
        """
        client = Client()
        # new_user sign-in with data2
        client.login(email=self.data2['email'],
                     password=self.data2['password1'])
        info_form_data = self.info.copy()
        info_form_data['first_name'] = '!'
        rendered_personal_info_form = EditPersonalInfo(info_form_data).render()
        info_form_data.update({'validate': 'true'})
        # submit first component form
        response = client.post(reverse('home:profile_form_view'), data=info_form_data, mode='same_origin')
        response_json = response.json()
        # check response 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['valid'], 'false')
        self.assertHTMLEqual(response_json['form'], rendered_personal_info_form)
        address_form_data = self.address.copy()
        address_form_data['county'] = '!'
        address_form_data.update({'validate': 'true'})
        rendered_address_form_data = EditAddress(address_form_data).render()
        # submit second component form
        response = client.post(reverse('home:profile_form_view'), data=address_form_data, mode='same_origin')
        response_json = response.json()
        # check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['valid'], 'false')
        self.assertHTMLEqual(response_json['form'], rendered_address_form_data)
        
    def test_response_post_request_profile_form_view_valid_forms_new_user(self):
        """
        Tests that a post request with valid form data, and using a new user, receives the expected responses.
        """
        client = Client()
        # new_user sign-in with data2
        client.login(email=self.data2['email'],
                     password=self.data2['password1'])
        info_form_data = self.info.copy()
        rendered_personal_info_form = EditPersonalInfo(info_form_data).render()
        info_form_data.update({'validate': 'true'})
        # submit first component form
        response = client.post(reverse('home:profile_form_view'), data=info_form_data, mode='same_origin')
        response_json = response.json()
        # check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['valid'], 'true')
        self.assertHTMLEqual(response_json['form'], rendered_personal_info_form)
        address_form_data = self.address.copy()
        address_form_data.update({'validate': 'true'})
        rendered_address_form_data = EditAddress(address_form_data).render()
        # submit second component form
        response = client.post(reverse('home:profile_form_view'), data=address_form_data, mode='same_origin')
        response_json = response.json()
        # check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['valid'], 'true')
        self.assertHTMLEqual(response_json['form'], rendered_address_form_data)
        info_form_data['validate'] = 'false'
        # send requests to save modelform instances for both valid component forms
        response = client.post(reverse('home:profile_form_view'), data=info_form_data, mode='same_origin')
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        address_form_data['validate'] = 'false'
        response = client.post(reverse('home:profile_form_view'), data=address_form_data, mode='same_origin')
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        # check the user profile section, and thus the various models, have been updated.
        rendered_home_page = client.get('/home/')
        self.assertContains(rendered_home_page, response_json['profile'], html=True)

    def test_response_post_request_profile_form_view_valid_forms_existing_user(self):
        """
        Tests that a post request with valid form data, and using an existing user, receives the expected responses.
        """
        client = Client()
        # existing user sign-in with data
        client.login(email=self.data['email'],
                     password=self.data['password1'])
        # submitting both forms unchanged to test all code bracnhes across all tests.
        info_form_data = self.info.copy()
        rendered_personal_info_form = EditPersonalInfo(info_form_data).render()
        info_form_data.update({'validate': 'true'})
        # submit first component form
        response = client.post(reverse('home:profile_form_view'), data=info_form_data, mode='same_origin')
        response_json = response.json()
        # check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['valid'], 'true')
        self.assertHTMLEqual(response_json['form'], rendered_personal_info_form)
        address_form_data = self.address.copy()
        address_form_data.update({'validate': 'true'})
        rendered_address_form_data = EditAddress(address_form_data).render()
        # submit second component form
        response = client.post(reverse('home:profile_form_view'), data=address_form_data, mode='same_origin')
        response_json = response.json()
        # check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['valid'], 'true')
        self.assertHTMLEqual(response_json['form'], rendered_address_form_data)
        info_form_data['validate'] = 'false'
        # send requests to save modelform instances for both valid component forms
        response = client.post(reverse('home:profile_form_view'), data=info_form_data, mode='same_origin')
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        address_form_data['validate'] = 'false'
        response = client.post(reverse('home:profile_form_view'), data=address_form_data, mode='same_origin')
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        # check the user profile section, and thus the various models, have been updated.
        rendered_home_page = client.get('/home/')
        self.assertContains(rendered_home_page, response_json['profile'], html=True)
        
    def test_response_post_request_profile_form_view_invalid_forms_existing_user(self):
        """
        Tests that a post request with invalid form data, and using an existing user, receives the expected responses.
        """
        client = Client()
        # existing user sign-in with data
        client.login(email=self.data['email'],
                     password=self.data['password1'])
        info_form_data = self.info.copy()
        info_form_data['first_name'] = '!'
        rendered_personal_info_form = EditPersonalInfo(info_form_data).render()
        info_form_data.update({'validate': 'true'})
        # submit first component form
        response = client.post(reverse('home:profile_form_view'), data=info_form_data, mode='same_origin')
        response_json = response.json()
        # check response 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['valid'], 'false')
        self.assertHTMLEqual(response_json['form'], rendered_personal_info_form)
        address_form_data = self.address.copy()
        address_form_data['county'] = '!'
        address_form_data.update({'validate': 'true'})
        rendered_address_form_data = EditAddress(address_form_data).render()
        # submit second component form
        response = client.post(reverse('home:profile_form_view'), data=address_form_data, mode='same_origin')
        response_json = response.json()
        # check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['valid'], 'false')
        self.assertHTMLEqual(response_json['form'], rendered_address_form_data)

    def test_response_post_request_profile_form_view_by_existing_user_for_api_error_(self):
        """
        Tests that a post request with valid form data for existing user, during an API related error, receives the expected responses.
        """
        client = Client()
        # existing user sign-in with data
        client.login(email=self.data['email'],
                     password=self.data['password1'])
        info_form_data = self.info.copy()
        info_form_data.update({'validate': 'true', 'bio': 'I like comedy events.'})
        # submit first component form
        response = client.post(reverse('home:profile_form_view'), data=info_form_data, mode='same_origin')
        response_json = response.json()
        address_form_data = self.address.copy()
        address_form_data.update({'validate': 'true', 'county': 20*'f', 'city_or_town': 20*'f',
                                  'address_line_one': 20*'f'})
        # submit second component form
        response = client.post(reverse('home:profile_form_view'), data=address_form_data, mode='same_origin')
        response_json = response.json()
        info_form_data['validate'] = 'false'
        # send requests to save modelform instances for both valid component forms
        response = client.post(reverse('home:profile_form_view'), data=info_form_data, mode='same_origin')
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        address_form_data['validate'] = 'false'
        response = client.post(reverse('home:profile_form_view'), data=address_form_data, mode='same_origin')
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        # check the user profile section, only has the personal info fields updated (user address fields should not change as instance not saved.)
        rendered_home_page = client.get('/home/')
        self.assertContains(rendered_home_page, response_json['profile'], html=True)
        
    def test_response_post_request_profile_form_view_by_new_user_for_api_error(self):
        """
        Tests that a post request with valid form data for new user, during an API related error, receives the expected responses.
        """
        client = Client()
        # new user sign-in with data2
        client.login(email=self.data2['email'],
                     password=self.data2['password1'])
        info_form_data = self.info.copy()
        info_form_data.update({'validate': 'true', 'bio': 'I like comedy events.'})
        # submit first component form
        response = client.post(reverse('home:profile_form_view'), data=info_form_data, mode='same_origin')
        response_json = response.json()
        address_form_data = self.address.copy()
        address_form_data.update({'validate': 'true', 'county': 20*'f', 'city_or_town': 20*'f',
                                  'address_line_one': 20*'f'})
        # submit second component form
        response = client.post(reverse('home:profile_form_view'), data=address_form_data, mode='same_origin')
        response_json = response.json()
        info_form_data['validate'] = 'false'
        # send requests to save modelform instances for both valid component forms
        response = client.post(reverse('home:profile_form_view'), data=info_form_data, mode='same_origin')
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        address_form_data['validate'] = 'false'
        response = client.post(reverse('home:profile_form_view'), data=address_form_data, mode='same_origin')
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        # check the user profile section unchanged as user profile instance deleted and user address instance not saved and so created.)
        rendered_home_page = client.get('/home/')
        self.assertContains(rendered_home_page, response_json['profile'], html=True)

    def test_response_get_fetch_request_profile_form_view(self):
        """
        Tests that a GET request for form refreshing, after closing the modal or clicking cancel, receives the expected responses.
        """
        client = Client()
        # existing user sign-in with data
        client.login(email=self.data['email'],
                     password=self.data['password1'])
        # retrieving the original edit profile modal content
        rendered_edit_profile_modal = client.get('/home/').context_data['edit_profile_modal']
        # GET request to reload the prefilled form values for the user
        response = client.get('/home/profile_form/?refresh=true&first_login=false', mode='same_origin')
        response_json = response.json()
        # checking the response status and its json payload
        self.assertEqual(response.status_code, 200)
        self.assertIn('modal', response_json)
        # Check that the prefilled values have been restored. CSRF's are different only.
        self.assertHTMLEqual(re.sub("(<input).+(name=\"csrf).+>", "", rendered_edit_profile_modal),
                             re.sub("(<input).+(name=\"csrf).+>", "", response_json['modal']))
