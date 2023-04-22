from django.test import TestCase
from django.test import Client
from django.core.validators import MaxLengthValidator
from django.core.exceptions import ValidationError
from django.forms import fields, boundfield
from django.template import Context, Template
from allauth.account.models import EmailAddress
from ..forms import Signup, Login

# Create your tests here.


class TestSignupForm(TestCase):
    """
    Tests the sign-up form.
    """
    def test_email_field_length_validators(self):
        """
        Tests that the correct length email field errors are raised for too long email inputs.
        """
        too_long_email1 = 'a@' + 254*'a' + 'e.com'
        too_long_email2 = 254*'a' + '@a.com'
        data1 = {'email': too_long_email1, 'email2': too_long_email1,
                 'password1': 'holly!123', 'password2': 'holly!123',
                 'username': 'jimmy'}
        form1 = Signup(data1)
        self.assertFalse(form1.is_valid())
        self.assertFormError(form=form1, field='email',
                             errors=['Enter a valid email address format.',
                                     'Email cannot be more than 254 characters.'])
        self.assertFormError(form=form1, field='email2', errors=[])
        data2 = {'email': too_long_email2, 'email2': too_long_email2,
                 'password1': 'holly!123', 'password2': 'holly!123',
                 'username': 'jimmy'}
        form2 = Signup(data2)
        self.assertFalse(form2.is_valid())
        self.assertFormError(form=form2, field='email',
                             errors=['Email cannot be more than 254 characters.'])
        self.assertFormError(form=form1, field='email2', errors=[])

    def test_email_fields_match_validation(self):
        """
        Tests that the email and retyped email matching error is raised when expected.
        """
        data = {'email': 'tommypaul@gmail.com',
                'email2': 'paul@gmail.com',
                'password1': 'holly!123',
                'password2': 'holly!123',
                'username': 'jimmy'}
        form = Signup(data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'email2',
                             ["Emails do not match."])
        data['email2'] = data['email']
        form = Signup(data)
        self.assertTrue(form.is_valid())
    
    def test_username_field_length_validation(self):
        """
        Tests that an error is raised when the username is too long.
        """
        data = {'email': 'tommypaul@gmail.com',
                'email2': 'tommypaul@gmail.com',
                'password1': 'holly!123',
                'password2': 'holly!123',
                'username': ''}

        def inner(length):
            data['username'] = length*'j'
            try:
                MaxLengthValidator(150)(data['username'])
                errors = []
            except ValidationError as err:
                errors = err.messages
            
            form = Signup(data)
            if length <= 150:
                self.assertTrue(form.is_valid())
            else:
                self.assertFalse(form.is_valid())
            self.assertFormError(form, 'username',
                                 errors)
        inner(151)
        inner(149)
    
    def test_valid_username_validation(self):
        """
        Tests that the UnicodeUsernameValidator is immplemented.
        """
        data = {'email': 'tommypaul@gmail.com',
                'email2': 'tommypaul@gmail.com',
                'password1': 'holly!123',
                'password2': 'holly!123',
                'username': 'jimmy$'}
        form = Signup(data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'username',
                             ["Enter a valid username. This value may contain only letters, "
                              "numbers, and @/./+/-/_ characters."])
        data['username'] = 'jimmy'
        form = Signup(data)
        self.assertTrue(form.is_valid())

    def test_username_field_unique_validator(self):
        """
        Tests that for a non-unique username input the expected error is raised.
        """
        client = Client()
        # sign-up new user
        data = {'email': 'tommypaul@gmail.com',
                'email2': 'tommypaul@gmail.com',
                'password1': 'holly!123',
                'password2': 'holly!123',
                'username': 'jimmy'}
        client.post('/accounts/signup/', data)
        # attempt sign-up new user with non-unique username
        data = {'email': 'tommy@gmail.com',
                'email2': 'tommy@gmail.com',
                'password1': 'holly!1235',
                'password2': 'holly!1235',
                'username': 'jimmy'}
        form = Signup(data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'username',
                             ['A user with this username already exists.'])
        # check no error is raised when unique username is provided
        data = {'email': 'tommy@gmail.com',
                'email2': 'tommy@gmail.com',
                'password1': 'holly!1235',
                'password2': 'holly!1235',
                'username': 'jimmy147'}
        form = Signup(data)
        self.assertTrue(form.is_valid())
        self.assertFormError(form, 'username', [])
        
    def test_password_length_validation(self):
        """
        Tests that the MinlengthValidator is immplemented and the expected error message is provided.
        """
        data = {'email': 'atommypaul@gmail.com',
                'email2': 'atommypaul@gmail.com',
                'password1': 'h1e2',
                'password2': 'h1e2',
                'username': 'timmy3'}
        form = Signup(data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'password1', 'This password is too short. It must contain at least 8 characters.')
        data['password1'] = '1325467h'
        data['password2'] = data['password1']
        form = Signup(data)
        self.assertTrue(form.is_valid())
        self.assertFormError(form, 'password1', [])

    def test_common_password_validation(self):
        """
        Tests that the django CommonPasswordValidator is immplemented and the expected error message is provided.
        """
        data = {'email': 'atommypaul@gmail.com',
                'email2': 'atommypaul@gmail.com',
                'password1': 'qwerty123',
                'password2': 'qwerty123',
                'username': 'timmy3'}
        form = Signup(data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'password1', 'This password is too commonly used.')
        data['password1'] = '1325467h'
        data['password2'] = data['password1']
        form = Signup(data)
        self.assertTrue(form.is_valid())
        self.assertFormError(form, 'password1', [])

    def test_password_similarity_validation(self):
        """
        Tests that the UserAttributeSimilarityValidator is immplemented and the expected error message is provided.
        """
        data = {'email': 'atommypaul@gmail.com',
                'email2': 'atommypaul@gmail.com',
                'password1': 'timmy137',
                'password2': 'timmy137',
                'username': 'timmy137'}
        form = Signup(data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'password1', 'The password is too similar to the username.')
        data['password1'] = '1325467h'
        data['password2'] = data['password1']
        form = Signup(data)
        self.assertTrue(form.is_valid())
        self.assertFormError(form, 'password1', [])
    
    def test_password_numeric_validation(self):
        """
        Tests that the NumericPasswordValidator is immplemented and the expected error message is provided.
        """
        data = {'email': 'atommypaul@gmail.com',
                'email2': 'atommypaul@gmail.com',
                'password1': '12348979',
                'password2': '12348979',
                'username': 'timmy137'}
        form = Signup(data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'password1', 'This password is entirely numeric.')
        data['password1'] = '1325467h'
        data['password2'] = data['password1']
        form = Signup(data)
        self.assertTrue(form.is_valid())
        self.assertFormError(form, 'password1', [])

    def test_password_fields_match_validation(self):
        """
        Tests that the password and retyped password matching error is raised when expected.
        """
        data = {'email': 'tommypaul@gmail.com',
                'email2': 'tommypaul@gmail.com',
                'password1': 'holly!123',
                'password2': 'olly!123',
                'username': 'jimmy'}
        form = Signup(data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'password2',
                             ["Passwords do not match."])
        data['password2'] = data['password1']
        form = Signup(data)
        self.assertTrue(form.is_valid())

    def test_required_field_validators(self):
        """
        Tests that an error is raised when a required field is left empty.
        """
        form = Signup({})
        for field_name, field in form.fields.items():
            if field.required:
                self.assertFormError(form, field_name, ['This field is required.'])
    
    def test_set_field_help_msg_method(self):
        """
        Ensures the set_field_help_msg method works.
        """
        form = Signup()
        self.assertEqual(form.fields['username'].help_text,
                         ('Must contain contain only letters, numbers, and @/./+/-/_ characters.'
                         ' Max 150 characters.'))
        self.assertEqual(form.fields['password1'].help_text,
                         'Must be at least 8 characters long, and include non-numeric characters.')
                         
    def test_set_field_styles_method(self):
        """
        Ensures the set_field_styles method works.
        """
        form = Signup({'username': 'jimmy649'})
        visible_fields = form.visible_fields()
        for field in visible_fields:
            with self.subTest(field.name):
                if field.name in form.errors:
                    self.assertEqual(field.css_classes, 'form_fields errors_present')
                else:
                    self.assertEqual(field.css_classes, 'form_fields')
    
    def test_signup_form_template_tags(self):
        """
        Tests that any newly added template tags to the modified django form template work.
        """
        def inner(tag_str, context_dict):
            return Template(tag_str).render(Context(context_dict))
        
        form = Signup()
        # 'field required if tag' tests
        field = boundfield.BoundField(form, fields.Field(), 'dummy')
        tag_str = '{% if field.field.required %}*{% endif %}'
        self.assertEqual(inner(tag_str, {'field': field}), '*')
        field = boundfield.BoundField(form, fields.Field(required=False), 'dummy')
        tag_str = '{% if field.field.required %}*{% endif %}'
        self.assertEqual(inner(tag_str, {'field': field}), '')
        # 'help_text if tag' tests
        tag_str = '{% if field.help_text %}<div class="help_text">{{ field.help_text|safe }}</div>{% endif %}'
        self.assertEqual(inner(tag_str, {'field': field}), '')
        field.help_text = 'help'
        self.assertEqual(inner(tag_str, {'field': field}), '<div class="help_text">help</div>')


class TestLoginForm(TestCase):
    """
    Tests the login form.
    """
    def test_set_field_styles_method(self):
        """
        Ensures the set_field_styles method works.
        """
        form = Login({'password': 'jimmy649'})
        visible_fields = form.visible_fields()
        for field in visible_fields:
            with self.subTest(field.name):
                if field.name in form.errors:
                    self.assertEqual(field.css_classes, 'form_fields errors_present')
                else:
                    self.assertEqual(field.css_classes, 'form_fields')
    
    def test_email_field_length_validators(self):
        """
        Tests that the correct length email field errors are raised for too long email inputs.
        """
        too_long_email1 = 'a@' + 254*'a' + 'e.com'
        too_long_email2 = 254*'a' + '@a.com'
        data1 = {'login': too_long_email1, 'password': 'jimmy123'}
        form1 = Login(data1)
        self.assertFalse(form1.is_valid())
        self.assertFormError(form=form1, field='login',
                             errors=['Enter a valid email address format.',
                                     'Email cannot be more than 254 characters.'])
        data2 = {'login': too_long_email2, 'password': 'jimmy123'}
        form2 = Login(data2)
        self.assertFalse(form2.is_valid())
        self.assertFormError(form=form2, field='login',
                             errors=['Email cannot be more than 254 characters.'])
    
    def test_authentication(self):
        """
        Tests that an error is displayed if the entered credentials do not
        match a registered user.
        """
        # Sign-up new user 
        client = Client()
        data = {'email': 'tommypaul147@gmail.com',
                'email2': 'tommypaul147@gmail.com',
                'password1': 'holly!123',
                'password2': 'holly!123',
                'username': 'jimmy147'}
        client.post('/accounts/signup/', data)
        # verify user email
        user = EmailAddress.objects.get(user='tommypaul147@gmail.com')
        user.verified = True
        user.save()
        # attempt user login: password wrong only
        data = {'login': 'tommypaul147@gmail.com', 'password': 'olly!123'}
        form = client.post('/accounts/login/', data).context_data['form']
        non_field_errors = form.get_context()['errors']
        self.assertFalse(form.is_valid())
        self.assertEqual(non_field_errors, ['The e-mail address and/or password you specified are not correct.'])
        # email wrong only
        data = {'login': 'tommypaul17@gmail.com', 'password': 'holly!123'}
        form = client.post('/accounts/login/', data).context_data['form']
        non_field_errors = form.get_context()['errors']
        self.assertFalse(form.is_valid())
        self.assertEqual(non_field_errors, ['The e-mail address and/or password you specified are not correct.'])
        # both wrong
        data = {'login': 'tommypaul17@gmail.com', 'password': 'olly!123'}      
        form = client.post('/accounts/login/', data).context_data['form']
        non_field_errors = form.get_context()['errors']
        self.assertFalse(form.is_valid())
        self.assertEqual(non_field_errors, ['The e-mail address and/or password you specified are not correct.'])
        # correct login
        response = client.login(email='tommypaul147@gmail.com', password='holly!123')
        self.assertTrue(response)
