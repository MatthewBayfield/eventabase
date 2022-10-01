from allauth.account.forms import SignupForm, BaseSignupForm
from django.forms.utils import ErrorList
from django.core.validators import EmailValidator, MaxLengthValidator

class Signup(SignupForm):
    """
    Sign-up form used for user registration.

    Essentially the same as the allauth SignupForm, with minor modifications
    affecting field validation, displayed error messages,
    field-styles, and displayed field help messages.

    Attributes:
        template_name (str): Sets the form template.
    """
    template_name = "account/signup_form.html"
    EmailValidator.message = ('Enter a valid email address format.')
    BaseSignupForm.declared_fields['email'].validators.append(MaxLengthValidator(254, 'Email cannot be more than 254 characters.'))

    def __init__(self, *args, **kwargs):
        """
        Form instance constructor.
        """
        super().__init__(*args, **kwargs)
        self.set_field_help_msg()
        if self.is_bound:
            self.set_field_error_msgs()
        self.set_field_styles()

    def set_field_styles(self):
        """
        Assigns css classes to form fields.
        """
        for tuple_obj in self.get_context()['fields']:
            boundfield = tuple_obj[0]
            boundfield.css_classes = 'form_fields'
            if tuple_obj[1] != "":
                boundfield.css_classes += " errors_present"

    def set_field_error_msgs(self):
        """
        Overrides default error messages of some field errors.
        """
        field_errors = self.errors

        try:
            email2_errors = field_errors.as_data()['email2']
            err_msgs = [error.message for error in email2_errors]
            err_msg = 'You must type the same email each time.'
            index = err_msgs.index(err_msg)
            email2_errors[index].message = 'Emails do not match.'
        except (ValueError, KeyError):
            pass
        try:
            email2_errors = field_errors.as_data()['email2']
            err_msgs = [error.message for error in email2_errors]
            err_msg = 'Enter a valid email address format.'
            index = err_msgs.index(err_msg)
            field_errors['email2'] = ErrorList(initlist=[error for error in email2_errors if error.message != err_msg])
        except (ValueError, KeyError):
            pass
        try:
            password2_errors = field_errors.as_data()['password2']
            err_msgs = [error.message for error in password2_errors]
            err_msg = 'You must type the same password each time.'
            index = err_msgs.index(err_msg)
            password2_errors[index].message = 'Passwords do not match.'
        except (ValueError, KeyError):
            pass
        try:
            password1_errors = field_errors.as_data()['password1']
            err_msgs = [error.message for error in password1_errors]
            err_msg = 'This password is too common.'
            index = err_msgs.index(err_msg)
            password1_errors[index].message = "This password is too commonly used."
        except (ValueError, KeyError):
            pass

    def set_field_help_msg(self):
        """
        Sets the help text of some form fields.
        """
        self.fields['username'].help_text = ('Must contain contain only letters, numbers, and @/./+/-/_ characters.'
                                             ' Max 150 characters.')
        self.fields['password1'].help_text = 'Must be at least 8 characters long, and include non-numeric characters.'






