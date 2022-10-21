import datetime
from django.test import TestCase
from landing_page.models import CustomUserModel
from ..models import UserAddress, UserProfile


class TestUserProfileModel(TestCase):
    """
    Tests for the UserProfile model.
    """
    info = {'first_name': 'Mark',
            'last_name': 'Taylor',
            'date_of_birth': '1993-11-19',
            'sex': 'male',
            'bio': 'I like sports'}

    def setUp(self):
        # create user
        username = 'taylor111'
        email = 'marktaylor@hotmail.com'
        password = 'alpha555'
        CustomUserModel.objects.create(username=username, email=email, password=password)

    def test_profile_instance_creation(self):
        """
        Tests that a profile instance is created as expected
        """
        user = CustomUserModel.objects.get(username='taylor111')
        # create core profile
        UserProfile.objects.create(user=user, first_name=self.info['first_name'],
                                   last_name=self.info['last_name'],
                                   date_of_birth=self.info['date_of_birth'],
                                   sex=self.info['sex'],
                                   bio=self.info['bio'])
        
        self.assertEqual(len(UserProfile.objects.filter(user=user)), 1)
        new_profile = UserProfile.objects.get(user=user)
        self.assertEqual(new_profile.first_name, self.info['first_name'])
        self.assertEqual(new_profile.last_name, self.info['last_name'])
        self.assertEqual(str(new_profile.date_of_birth), self.info['date_of_birth'])
        self.assertEqual(new_profile.sex, self.info['sex'])
        self.assertEqual(new_profile.bio, self.info['bio'])

    def test_inherited_mixin_methods(self):
        """
        Tests that the ProfileMixin methods work as expected for the UserProfile model.
        """
        # testing retrieve_field_names class method
        expected_names = ['address', 'user', 'first_name', 'last_name', 'date_of_birth', 'sex', 'bio']
        self.assertEqual(UserProfile.retrieve_field_names(False), expected_names)
        expected_verbose_names = ['address', 'user', 'first name', 'last name', 'date of birth', 'sex', 'bio']
        self.assertEqual(UserProfile.retrieve_field_names(), expected_verbose_names)
        # testing retrieve_field_data method
        user = CustomUserModel.objects.get(username='taylor111')
        UserProfile.objects.create(user=user, first_name=self.info['first_name'],
                                   last_name=self.info['last_name'],
                                   date_of_birth=self.info['date_of_birth'],
                                   sex=self.info['sex'],
                                   bio=self.info['bio'])
        new_profile = UserProfile.objects.get(user=user)
        expected_verbose_data = {'address': None,
                                 'user': user,
                                 'first name': 'Mark',
                                 'last name': 'Taylor',
                                 'date of birth': datetime.date(1993, 11, 19),
                                 'sex': 'male', 'bio': 'I like sports'}
        self.assertEqual(new_profile.retrieve_field_data(), expected_verbose_data)
        expected_data = {'address': None, 'user': user,
                         'first_name': 'Mark',
                         'last_name': 'Taylor',
                         'date_of_birth': datetime.date(1993, 11, 19),
                         'sex': 'male',
                         'bio': 'I like sports'}
        self.assertEqual(new_profile.retrieve_field_data(False), expected_data)


class TestUserAddressModel(TestCase):
    """
    Tests for the UserAddress model.
    """
    info = {'first_name': 'Mark',
            'last_name': 'Taylor',
            'date_of_birth': '1993-11-19',
            'sex': 'male',
            'bio': 'I like sports'}
    address = {'address_line_one': '58 stanley avenue',
               'city_or_town': 'gidea park',
               'county': 'essex',
               'postcode': 'rm26bt',
               'latitude': 51.5811,
               'longitude': 0.2059}

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

    def test_address_instance_creation(self):
        """
        Tests that a profile instance is created as expected
        """
        profile = UserProfile.objects.get(user__username='taylor111')
        # create address
        UserAddress.objects.create(user_profile=profile, address_line_one=self.address['address_line_one'],
                                   city_or_town=self.address['city_or_town'],
                                   county=self.address['county'],
                                   postcode=self.address['postcode'],
                                   latitude=self.address['latitude'],
                                   longitude=self.address['longitude'])
        
        self.assertEqual(len(UserAddress.objects.filter(user_profile=profile)), 1)
        new_address = UserAddress.objects.get(user_profile=profile)
        self.assertEqual(new_address.address_line_one, self.address['address_line_one'])
        self.assertEqual(new_address.city_or_town, self.address['city_or_town'])
        self.assertEqual(new_address.county, self.address['county'])
        self.assertEqual(new_address.postcode, self.address['postcode'])
        print(float(new_address.latitude))
        self.assertEqual(float(new_address.latitude), self.address['latitude'])
        self.assertEqual(float(new_address.longitude), self.address['longitude'])

    def test_inherited_mixin_methods(self):
        """
        Tests that the ProfileMixin methods work as expected for the UserAddress model.
        """
        # testing retrieve_field_names class method
        expected_names = ['user_profile', 'address_line_one', 'city_or_town', 'county', 'postcode', 'latitude', 'longitude']
        self.assertEqual(UserAddress.retrieve_field_names(False), expected_names)
        expected_verbose_names = ['user profile', 'Address line 1', 'City/Town', 'County', 'Postcode', 'latitude', 'longitude']
        self.assertEqual(UserAddress.retrieve_field_names(), expected_verbose_names)
        # # testing retrieve_field_data method
        user = CustomUserModel.objects.get(username='taylor111')
        new_profile = UserProfile.objects.get(user=user)
        new_address = UserAddress.objects.create(user_profile=new_profile,
                                                 address_line_one=self.address['address_line_one'],
                                                 city_or_town=self.address['city_or_town'],
                                                 county=self.address['county'],
                                                 postcode=self.address['postcode'],
                                                 latitude=self.address['latitude'],
                                                 longitude=self.address['longitude'])
        expected_verbose_data = {'user profile': new_profile,
                                 'Address line 1': '58 stanley avenue',
                                 'City/Town': 'gidea park',
                                 'County': 'essex',
                                 'Postcode': 'rm26bt',
                                 'latitude': 51.5811,
                                 'longitude': 0.2059}
        self.assertEqual(new_address.retrieve_field_data(), expected_verbose_data)
        expected_data = {'user_profile': new_profile,
                         'address_line_one': '58 stanley avenue',
                         'city_or_town': 'gidea park',
                         'county': 'essex',
                         'postcode': 'rm26bt',
                         'latitude': 51.5811,
                         'longitude': 0.2059}
        self.assertEqual(new_address.retrieve_field_data(False), expected_data)

