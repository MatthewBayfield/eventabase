from django.test import TestCase
from django.utils import timezone
from ..models import CustomUserModel

# Create your tests here.


class TestCustomUserModel(TestCase):
    """
    Tests for the CustomUserModel
    """

    def test_user_creation(self):
        """
        Tests that a user instance is created as expected
        """
        username = 'taylor111'
        email = 'marktaylor@hotmail.com'
        password = 'alpha555'
        CustomUserModel.objects.create(username=username, email=email, password=password)
        self.assertEqual(len(CustomUserModel.objects.filter(email=email)), 1)
        new_user = CustomUserModel.objects.get(email=email)
        self.assertEqual(new_user.email, email)
        self.assertEqual(new_user.username, username)
        self.assertEqual(new_user.is_active, True)
        self.assertEqual(new_user.is_staff, False)
        self.assertEqual(new_user.is_superuser, False)
        self.assertEqual(new_user.date_joined.date(), timezone.now().date())


