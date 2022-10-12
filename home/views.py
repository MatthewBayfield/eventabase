from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import get_template
from allauth.account.decorators import verified_email_required

# Create your views here.

@method_decorator(verified_email_required, name='dispatch')
class UserHomePage(TemplateView):
    """
    View for the user home page.
    """
    template_name = "home/home.html"
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.extra_context)
        return context

    def is_user_staff(self):
        return self.request.user.is_staff

    def retrieve_profile_from_request(self):
        """
        Returns a queryset containing a users profile if one exists.
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
            self.extra_context.update({'username': self.request.user.username})
            user_profile = self.retrieve_profile_from_request()
            user_profile_data = user_profile.retrieve_field_data() if user_profile else {}
            if user_profile:
                first_login = False
                user_profile_data.pop('username')
                user_address = user_profile_data.pop('address')
                user_address_data = user_address.retrieve_field_data()
                for field in ['username', 'latitude', 'longitude']:
                    user_address_data.pop(field)
                profile_template = get_template('home/profile.html')
                rendered_profile_template = profile_template.render({'user_profile_data': user_profile_data.items(),
                                                                     'user_address_data': user_address_data.items()})
                self.extra_context.update({'profile': rendered_profile_template})
            else:
                first_login = True
                pass
        return super().get(request, *args, **kwargs)
