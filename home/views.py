from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import get_template, render_to_string
from allauth.account.decorators import verified_email_required
from .forms import EditAddress, EditPersonalInfo
from .models import UserProfile, UserAddress

# Create your views here.

class HomeViewsMixin():
    """
    Features methods for retrieving a user's profile from a request, and for rendering the profile template.

    Attributes:
        profile_template (template): the profile template used for rendering.
    """
    profile_template = get_template('home/profile.html')

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
            
    def render_profile_template(self, to_string=False):
        """
        Renders the profile template for a user's homepage.

        Either renders to string or renders to response for different end purposes.

        Args:
            to_string (boolean): determines the profile render method used.

        Returns:
            A list containing the rendered profile, the user profile instance, and the user address instance.
        """
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
            self.first_login = True
            user_profile_data = UserProfile.retrieve_field_names()
            user_profile_data = {key: '' for key in user_profile_data}
            user_profile_data.pop('user')
            user_address = user_profile_data.pop('address')
            user_address_data = UserAddress.retrieve_field_names()
            user_address_data = {key: '' for key in user_address_data}
            for field in ['user profile', 'latitude', 'longitude']:
                user_address_data.pop(field)

        if not to_string:
            rendered_profile_template = self.profile_template.render({'user_profile_data': user_profile_data.items(),
                                                                      'user_address_data': user_address_data.items()})
        else:
            rendered_profile_template = render_to_string(template_name='home/profile.html',
                                                         context={'user_profile_data': user_profile_data.items(),
                                                                  'user_address_data': user_address_data.items()})

        self.further_context.update({'profile': rendered_profile_template})
        return [rendered_profile_template, user_profile, user_address]


@method_decorator(verified_email_required, name='dispatch')
class UserHomePage(TemplateView, HomeViewsMixin):
    """
    View for the user home page. Responsible for retrieving core information and allowing key site activity.

    Attributes:
        template_name (str): name of the template used to render the home page.
        first_login (boolean): indicates whether the user has logged in before.
        further_context (dict): contains context used in rendering the template.
    """
    template_name = "home/home.html"

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

    def get(self, request, *args, **kwargs):
        """
        Handles GET request.

        Returns:
            A HTTP response containing the rendered with context home page template.
        """
        if self.is_user_staff():
            pass
        else:
            self.further_context.update({'username': self.request.user.username,
                                         'button1_name': 'Done',
                                         'button2_name': 'Cancel'})
            rendered_profile_template, user_profile, user_address = self.render_profile_template()
            
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
class ProfileFormView(FormView, HomeViewsMixin):
    """
    Generates the initial profile modal form for a user, and processes form submission and profile updating.

    Attributes:
        modal_template (template): the template used to render the edit profile modal.
        initial (dict): contains the initial form data to prepopulate a form.
        first_login (boolean): indicates whether the user has logged in before.
        further_context (dict): contains context used in rendering the template.
        form_class (form): The default form class.
    """
    prefix = None
    modal_template = get_template('home/edit_profile_modal.html')

    def __init__(self, **kwargs):
        """
        Calls the TemplateView constructor. Sets initial context.
        Creates initial form data dictionary and default form class.
        """
        super().__init__(**kwargs)
        self.initial = {}
        self.form_class = EditPersonalInfo
        self.first_login = True
        self.further_context = {'first_login': self.first_login}

    def get(self, request, *args, **kwargs):
        """
        Handles GET request for edit profile form.

        Returns:
            Either an empty modal form, or a prepopulated form if the user already has a profile.
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
        Handles edit profile form submission and processing. Carries out profile and address model updates.

        Returns:
            Several possible JSON responses to a fetch request, indicating the submitted component forms validity,
            and returning a rendered string of the processed forms or the rendered profile.
        """
        personal_info_form_data = None
        address_form_data = None
        data = {}
        rendered_profile_template = None

        if 'first_name' in request.POST:
            personal_info_form_data = request.POST
        else:
            address_form_data = request.POST

        user = self.request.user
        user_profile = UserProfile.objects.filter(user=user).exists()
        if personal_info_form_data:
            if user_profile:
                self.first_login = False
                user_profile = user.profile
                form = EditPersonalInfo(data=personal_info_form_data, instance=user_profile)
            else:
                self.first_login = True
                form = EditPersonalInfo(data=personal_info_form_data)

            if request.POST['validate'] == 'true':
                if form.is_valid():
                    rendered_form = render_to_string(template_name='home/edit_profile_form.html', context=form.get_context(), request=request)
                    return JsonResponse({'valid': 'true', 'form': rendered_form})      
            else:
                if form.has_changed():
                    form.post_clean_processing(user=user)
                    form.save()

        elif address_form_data:
            if user_profile:
                self.first_login = False
                user_profile = user.profile
                if UserAddress.objects.filter(user_profile=user_profile).exists():
                    user_address = user.profile.address
                    form = EditAddress(data=address_form_data, instance=user_address)
                else:
                    self.first_login = True
                    form = EditAddress(data=address_form_data)
            else:
                self.first_login = True
                form = EditAddress(data=address_form_data)
            if request.POST['validate'] == 'true':
                if form.is_valid():
                    rendered_form = render_to_string(template_name='home/edit_profile_form.html', context=form.get_context(), request=request)
                    return JsonResponse({'valid': 'true', 'form': rendered_form})
            else:
                if form.has_changed():
                    form.post_clean_processing(user_profile=user_profile)
                    form.set_coordintes()
                    form.save()
                rendered_profile_template = self.render_profile_template(to_string=True)[0]
                trimmed_rendered_profile_template = rendered_profile_template[rendered_profile_template.index('<div class="left'):-6]
                data.update({'profile': trimmed_rendered_profile_template})
        rendered_form = render_to_string(template_name='home/edit_profile_form.html', context=form.get_context(), request=request)
        data.update({'form': rendered_form, 'valid': 'false'})
        return JsonResponse(data)
