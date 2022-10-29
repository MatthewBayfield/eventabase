from datetime import date
from unittest.mock import patch
from django.test import TestCase
from landing_page.models import CustomUserModel
from ..forms import EditAddress, EditPersonalInfo
from ..models import UserAddress, UserProfile


class TestEditPersonalInfoForm(TestCase):
    """
    Tests for the EditPersonalInfo model form.
    """
    info = {'first_name': 'Mark',
            'last_name': 'Taylor',
            'date_of_birth': '19/11/1993',
            'sex': 'male',
            'bio': 'I like sports'}
    post_processed_info = {'first_name': 'mark',
                           'last_name': 'taylor',
                           'date_of_birth': date(1993, 11, 19),
                           'sex': 'male',
                           'bio': 'I like sports'}
    edit_info = {'first_name': 'JASON',
                 'last_name': 'Taylor',
                 'date_of_birth': '19/11/1993',
                 'sex': 'male',
                 'bio': "I don't like sports."}

    def setUp(self):
        # create user
        username = 'taylor111'
        email = 'marktaylor@hotmail.com'
        password = 'alpha555'
        CustomUserModel.objects.create(username=username, email=email, password=password)
        user = CustomUserModel.objects.get(username='taylor111')

    def test_first_name_field_validators(self):
        """
        Tests that the first_name validators are applied and expected errors added to the form context.
        """
        info = self.info.copy()
        user = CustomUserModel.objects.get(username='taylor111')
        info.update({'user': user})
        # test regrex validator
        info['first_name'] = 'mar!k'
        new_form = EditPersonalInfo(data=info)
        valid = new_form.is_valid()
        self.assertFalse(valid)
        self.assertFormError(new_form, 'first_name', "Must contain only standard alphabetic characters.")
        # test maxlength validator
        info['first_name'] = 51*'m'
        new_form = EditPersonalInfo(data=info)
        valid = new_form.is_valid()
        self.assertFalse(valid)
        self.assertFormError(new_form, 'first_name', 'Ensure this value has at most 50 characters (it has 51).')
    
    def test_last_name_field_validators(self):
        """
        Tests that the last_name validators are applied and expected errors added to the form context.
        """
        info = self.info.copy()
        user = CustomUserModel.objects.get(username='taylor111')
        info.update({'user': user})
        # test regrex validator
        info['last_name'] = 'tay lor'
        new_form = EditPersonalInfo(data=info)
        valid = new_form.is_valid()
        self.assertFalse(valid)
        self.assertFormError(new_form, 'last_name', "Must contain only standard alphabetic characters.")
        # test maxlength validator
        info['last_name'] = 51*'t'
        new_form = EditPersonalInfo(data=info)
        valid = new_form.is_valid()
        self.assertFalse(valid)
        self.assertFormError(new_form, 'last_name', 'Ensure this value has at most 50 characters (it has 51).')

    def test_date_of_birth_field_validators(self):
        """
        Tests that the date_of_birth validators are applied and expected errors added to the form context.
        """
        info = self.info.copy()
        user = CustomUserModel.objects.get(username='taylor111')
        info.update({'user': user})
        # test format validator
        info['date_of_birth'] = '19/11/93'
        new_form = EditPersonalInfo(data=info)
        valid = new_form.is_valid()
        self.assertFalse(valid)
        self.assertFormError(new_form, 'date_of_birth', 'Enter a valid date format.')

    def test_bio_field_validators(self):
        """
        Tests that the bio field validators are applied and expected errors added to the form context.
        """
        info = self.info.copy()
        user = CustomUserModel.objects.get(username='taylor111')
        info.update({'user': user})
        # test maxlength validator
        info['bio'] = 501*'r'
        new_form = EditPersonalInfo(data=info)
        valid = new_form.is_valid()
        self.assertFalse(valid)
        self.assertFormError(new_form, 'bio', 'Ensure this value has at most 500 characters (it has 501).')

    def test_the_post_clean_processing_method(self):
        """
        Tests the method works.
        """
        user = CustomUserModel.objects.get(username='taylor111')
        self.info.update({'user': user})
        self.post_processed_info.update({'user': user})
        # create valid form from info dict
        new_form = EditPersonalInfo(data=self.info)
        # check form is valid, as it should be using self.info
        valid = new_form.is_valid()
        self.assertTrue(valid)
        new_form.post_clean_processing(user=user)
        for field_name, value in self.post_processed_info.items():
            received = getattr(new_form.instance, field_name)
            self.assertEqual(received, value)

    def test_personal_info_form_instance_creation(self):
        """
        Tests that a new profile instance is created for a valid form.
        """
        user = CustomUserModel.objects.get(username='taylor111')
        # assert the profile does not already exist
        self.assertFalse(UserProfile.objects.filter(user=user).exists())
        self.info.update({'user': user})
        # create valid form from info dict
        new_form = EditPersonalInfo(data=self.info)
        # check form is valid, as it should be using self.info
        valid = new_form.is_valid()
        self.assertTrue(valid)
        new_form.post_clean_processing(user=user)
        # save the instance and check it now exits    
        new_form.save()
        self.assertTrue(UserProfile.objects.filter(user=user).exists())

    def test_personal_info_form_instance_creation_for_update(self):
        """
        Tests that an existing profile instance is updated when using a valid form.
        """
        # create profile instance
        user = CustomUserModel.objects.get(username='taylor111')
        self.info.update({'user': user})
        new_form = EditPersonalInfo(data=self.info)
        new_form.post_clean_processing(user=user)   
        new_form.save()
        # assert the profile just created exists
        self.assertTrue(UserProfile.objects.filter(user=user).exists())
        # update the profile using a valid form:
        user_profile = UserProfile.objects.get(user=user)
        new_form = EditPersonalInfo(data=self.edit_info, instance=user_profile)
        valid = new_form.is_valid()
        self.assertTrue(valid)
        new_form.post_clean_processing(user=user) 
        new_form.save()
        self.assertTrue(UserProfile.objects.filter(user=user).exists())
        user_profile = UserProfile.objects.get(user=user)
        # check that edited fields have been updated.
        self.assertEqual(user_profile.first_name, 'jason')
        self.assertEqual(user_profile.bio, "I don't like sports.")

    def test_set_field_styles_method(self):
        """
        Ensures the set_field_styles method works.
        """
        new_form = EditPersonalInfo({'first_name': 'M!ark',
                                'last_name': 'T aylor',
                                'date_of_birth': '19111993',
                                'sex': 'male',
                                'bio': 'I like sports.'})
        visible_fields = new_form.visible_fields()
        for field in visible_fields:
            with self.subTest(field.name):
                if field.name in new_form.errors:
                    self.assertEqual(field.css_classes, 'form_fields errors_present')
                else:
                    self.assertEqual(field.css_classes, 'form_fields')
        
    def test_set_field_help_msg_method(self):
        """
        Ensures the set_field_help_msg method works.
        """
        form = EditPersonalInfo()
        self.assertEqual(form.fields['date_of_birth'].help_text, 'Enter a date in the format dd/mm/yyyy.')
        self.assertEqual(form.fields['bio'].help_text,
                         'Describe a bit about yourself, and or the activities you like. Max 500 characters.')

    def test_required_field_validators(self):
        """
        Tests that an error is raised when a required field is left empty.
        """
        form = EditPersonalInfo({})
        for field_name, field in form.fields.items():
            if field.required:
                self.assertFormError(form, field_name, ['This field is required.'])


class TestEditAddressForm(TestCase):
    """
    Tests for the EditAddress model form.
    """
    info = {'first_name': 'mark',
            'last_name': 'taylor',
            'date_of_birth': '1993-11-19',
            'sex': 'male',
            'bio': 'I like sports'}
    address = {'address_line_one': '58 Stanley Avenue',
               'city_or_town': 'GIdea Park',
               'county': 'ESSEX',
               'postcode': 'Rm26Bt'}
    post_processed_address = {'address_line_one': '58 stanley avenue',
                              'city_or_town': 'gidea park',
                              'county': 'essex',
                              'postcode': 'rm26bt'}
    edit_address = {'address_line_one': '60 crawley lane',
                    'city_or_town': 'GIdea Park',
                    'county': 'KENT',
                    'postcode': 'Rm26Bt'}

    def setUp(self):
        # create user
        username = 'taylor111'
        email = 'marktaylor@hotmail.com'
        password = 'alpha555'
        CustomUserModel.objects.create(username=username, email=email, password=password)
        user = CustomUserModel.objects.get(username='taylor111')
        # create core profile
        UserProfile.objects.create(user=user, first_name=self.info['first_name'],
                                   last_name=self.info['last_name'],
                                   date_of_birth=self.info['date_of_birth'],
                                   sex=self.info['sex'],
                                   bio=self.info['bio'])
    
    def test_address_line_one_field_validators(self):
        """
        Tests that the address_line_one validators are applied and expected errors added to the form context.
        """
        address = self.address.copy()
        profile = UserProfile.objects.get(user__username='taylor111')
        address.update({'user_profile': profile})
        # test regrex validator
        address['address_line_one'] = '11 rise park     boulevard'
        new_form = EditAddress(data=address)
        valid = new_form.is_valid()
        self.assertFalse(valid)
        self.assertFormError(new_form, 'address_line_one', "Must contain only standard alphabetic characters and numbers, with single spaces between words.")
        # test maxlength validator
        address['address_line_one'] = 101*'t'
        new_form = EditAddress(data=address)
        valid = new_form.is_valid()
        self.assertFalse(valid)
        self.assertFormError(new_form, 'address_line_one', 'Ensure this value has at most 100 characters (it has 101).')

    def test_city_or_town_field_validators(self):
        """
        Tests that the city_or_town field validators are applied and expected errors added to the form context.
        """
        address = self.address.copy()
        profile = UserProfile.objects.get(user__username='taylor111')
        address.update({'user_profile': profile})
        # test regrex validator
        address['city_or_town'] = 'dageham3'
        new_form = EditAddress(data=address)
        valid = new_form.is_valid()
        self.assertFalse(valid)
        self.assertFormError(new_form, 'city_or_town', "Must contain only standard alphabetic characters, with single spaces between words.")
        # test maxlength validator
        address['city_or_town'] = 51*'t'
        new_form = EditAddress(data=address)
        valid = new_form.is_valid()
        self.assertFalse(valid)
        self.assertFormError(new_form, 'city_or_town', 'Ensure this value has at most 50 characters (it has 51).')

    def test_county_field_validators(self):
        """
        Tests that the county field validators are applied and expected errors added to the form context.
        """
        address = self.address.copy()
        profile = UserProfile.objects.get(user__username='taylor111')
        address.update({'user_profile': profile})
        # test regrex validator
        address['county'] = 'esse  x'
        new_form = EditAddress(data=address)
        valid = new_form.is_valid()
        self.assertFalse(valid)
        self.assertFormError(new_form, 'county', "Must contain only standard alphabetic characters, with single spaces between words.")
        # test maxlength validator
        address['county'] = 51*'t'
        new_form = EditAddress(data=address)
        valid = new_form.is_valid()
        self.assertFalse(valid)
        self.assertFormError(new_form, 'county', 'Ensure this value has at most 50 characters (it has 51).')

    def test_postcode_field_validators(self):
        """
        Tests that the postcode field validators are applied and expected errors added to the form context.
        """
        address = self.address.copy()
        profile = UserProfile.objects.get(user__username='taylor111')
        address.update({'user_profile': profile})
        # test regrex validator
        address['postcode'] = 'r345 6pl'
        new_form = EditAddress(data=address)
        valid = new_form.is_valid()
        self.assertFalse(valid)
        self.assertFormError(new_form, 'postcode', "Must be a valid postcode format.")

    def test_the_post_clean_processing_method(self):
        """
        Tests the method works.
        """
        profile = UserProfile.objects.get(user__username='taylor111')
        self.address.update({'user_profile': profile})
        self.post_processed_address.update({'user_profile': profile})
        # create valid form from address dict
        new_form = EditAddress(data=self.address)
        # check form is valid, as it should be using self.address
        valid = new_form.is_valid()
        self.assertTrue(valid)
        new_form.post_clean_processing(user_profile=profile)
        for field_name, value in self.post_processed_address.items():
            received = getattr(new_form.instance, field_name)
            self.assertEqual(received, value)
    
    @patch('home.forms.requests')
    def test_the_set_coordinates_method(self, mock_requests):
        """
        Tests that the method works as expected.
        """
        url = 'https://api.geoapify.com/v1/geocode/search?text=58%20stanley%20avenue%2C%20gidea%20park%2C%20essex%2C%20rm26bt&lang=en&filter=countrycode:gb&format=json&apiKey=9ecb78e37e4c446a80037538de50e34b'
        headers = {'Accept': 'application/json'}
        profile = UserProfile.objects.get(user__username='taylor111')
        self.address.update({'user_profile': profile})
        # create valid form from address dict
        new_form = EditAddress(data=self.address)
        # check form is valid, as it should be using self.address
        valid = new_form.is_valid()
        self.assertTrue(valid)
        new_form.post_clean_processing(user_profile=profile)
        new_form.set_coordintes()
        mock_requests.get.assert_called_once_with(url, headers=headers)
        # default return_value of __float__ MagicMock object magic method is 1.0
        self.assertEqual(new_form.instance.latitude, 1.0)
        self.assertEqual(new_form.instance.longitude, 1.0)

    def test_address_form_instance_creation(self):
        """
        Tests that a new address instance is created as expected when using a valid form.
        """
        profile = UserProfile.objects.get(user__username='taylor111')
        # assert the address does not already exist
        self.assertFalse(UserAddress.objects.filter(user_profile=profile).exists())
        self.address.update({'user_profile': profile})
        # create valid form from address dict
        new_form = EditAddress(data=self.address)
        # check form is valid, as it should be using self.address
        valid = new_form.is_valid()
        self.assertTrue(valid)
        new_form.post_clean_processing(user_profile=profile)
        new_form.set_coordintes()
        # save the instance and check it now exits    
        new_form.save()
        self.assertTrue(UserAddress.objects.filter(user_profile=profile).exists())

    def test_edit_address_form_instance_creation_for_update(self):
        """
        Tests that an existing address instance is updated when using a valid form.
        """
        profile = UserProfile.objects.get(user__username='taylor111')
        new_form = EditAddress(data=self.address)
        new_form.post_clean_processing(user_profile=profile)
        new_form.set_coordintes()
        new_form.save()
        # assert that the just created address instance exists
        self.assertTrue(UserAddress.objects.filter(user_profile=profile).exists())
        # update the address using a valid form:
        address = UserAddress.objects.get(user_profile=profile)
        new_form = EditAddress(data=self.edit_address, instance=address)
        valid = new_form.is_valid()
        self.assertTrue(valid)
        new_form.post_clean_processing(user_profile=profile)
        new_form.set_coordintes()
        new_form.save()
        self.assertTrue(UserAddress.objects.filter(user_profile=profile).exists())
        address = UserAddress.objects.get(user_profile=profile)
        # check that edited fields have been updated.
        self.assertEqual(address.address_line_one, '60 crawley lane')
        self.assertEqual(address.county, "kent")

    def test_set_field_styles_method(self):
        """
        Ensures the set_field_styles method works.
        """
        new_form = EditAddress({'address_line_one': '58 Stanley Avenue',
                                'city_or_town': 'G Idea Park',
                                'county': 'ESS56EX',
                                'postcode': 'zRm26Bt'})
        visible_fields = new_form.visible_fields()
        for field in visible_fields:
            with self.subTest(field.name):
                if field.name in new_form.errors:
                    self.assertEqual(field.css_classes, 'form_fields errors_present')
                else:
                    self.assertEqual(field.css_classes, 'form_fields')
    
    def test_required_field_validators(self):
        """
        Tests that an error is raised when a required field is left empty.
        """
        form = EditAddress({})
        for field_name, field in form.fields.items():
            if field.required:
                self.assertFormError(form, field_name, ['This field is required.'])
