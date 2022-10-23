from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import get_template
from allauth.account.decorators import verified_email_required
from .forms import EditAddress, EditPersonalInfo
from .models import UserProfile, UserAddress

# Create your views here.

@method_decorator(verified_email_required, name='dispatch')
class UserHomePage(TemplateView):
    """
    View for the user home page.
    """
    template_name = "home/home.html"
    profile_template = get_template('home/profile.html')

    def __init__(self, **kwargs):
        """
        Calls the TemplateView constructor. Sets initial context.
        """
        super().__init__(**kwargs)
        self.first_login = True
        self.further_context = {'first_login': self.first_login}
        
    def get_context_data(self, **kwargs):
        """
        Amalgamates context data.

        Args:
            kwargs (dict)

        Returns:
            context dictionary.
        """
        context = super().get_context_data(**kwargs)
        context.update(self.further_context)
        return context

    def is_user_staff(self):
        """
        Returns a boolean indicating whether the authenticated user is staff.
        """
        return self.request.user.is_staff

    def retrieve_profile_from_request(self):
        """
        Returns a user's profile if one exists or None.

        Raises:
            ObjectDoesNotExist: if a profile does not exist.
        """
        user = self.request.user
        try:
            return user.profile
        except ObjectDoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        """
        Handles GET request.
        """
        if self.is_user_staff():
            pass
        else:
            self.further_context.update({'username': self.request.user.username,
                                         'button1_name': 'Done',
                                         'button2_name': 'Cancel'})
            user_profile = self.retrieve_profile_from_request()
            if user_profile:
                user_profile_data = user_profile.retrieve_field_data()
                user_profile_data['date of birth'] = user_profile_data['date of birth'].strftime('%d/%m/%Y')
                self.first_login = False
                self.further_context['first_login'] = self.first_login
                user_profile_data.pop('user')
                user_address = user_profile_data.pop('address')
                user_address_data = user_address.retrieve_field_data()
                for field in ['user profile', 'latitude', 'longitude']:
                    user_address_data.pop(field)
            else:
                user_profile_data = UserProfile.retrieve_field_names()
                user_profile_data = {key: '' for key in user_profile_data}
                user_profile_data.pop('user')
                user_address = user_profile_data.pop('address')
                user_address_data = UserAddress.retrieve_field_names()
                user_address_data = {key: '' for key in user_address_data}
                for field in ['user profile', 'latitude', 'longitude']:
                    user_address_data.pop(field)
            
            rendered_profile_template = self.profile_template.render({'user_profile_data': user_profile_data.items(),
                                                                      'user_address_data': user_address_data.items()})
            self.further_context.update({'profile': rendered_profile_template})
            
            self.get_context_data(**kwargs)
            kwargs.update(self.further_context)
            rendered_edit_profile_modal = ProfileFormView.as_view()(request,
                                                                    *args,
                                                                    user_profile=user_profile,
                                                                    user_address=user_address,
                                                                    modal='edit_profile_modal',
                                                                    **kwargs)
            kwargs.update({'edit_profile_modal': rendered_edit_profile_modal})
            return super().get(request, *args, **kwargs)

@method_decorator(verified_email_required, name='dispatch')
class ProfileFormView(FormView):
    """
    """
    prefix = None
    modal_template = get_template('home/edit_profile_modal.html')

    def __init__(self, **kwargs):
        """
        """
        super().__init__(**kwargs)
        self.initial = {}
        self.form_class = EditPersonalInfo

    def get(self, request, *args, **kwargs):
        """
        Handles GET request.
        """
        if request.path != reverse('home:user_homepage'):
            return redirect(reverse('home:user_homepage'))

        if not kwargs['first_login']:
            self.initial = kwargs['user_profile'].retrieve_field_data(False)
            unformatted_date = self.initial['date_of_birth']
            self.initial['date_of_birth'] = unformatted_date.strftime('%d/%m/%Y')
            form = self.get_form()
            kwargs.update({'personal_info_form': form})

            self.initial.update(kwargs['user_address'].retrieve_field_data(False))
            self.form_class = EditAddress
            form = self.get_form()
            kwargs.update({'address_form': form})
        else:
            form = self.get_form()
            kwargs.update({'personal_info_form': form})
            self.form_class = EditAddress
            form = self.get_form()
            kwargs.update({'address_form': form})

        rendered_modal_template = self.modal_template.render(kwargs, request)
        return rendered_modal_template
            
    def post(self, request, *args, **kwargs):
        """
        Handles POST request.
        """