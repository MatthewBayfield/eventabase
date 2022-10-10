from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
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

    def get(self, request, *args, **kwargs):
        """
        Handles GET request.
        """
        if self.is_user_staff():
            pass
        else:
            self.extra_context.update({'username': self.request.user.username})
        return super().get(request, *args, **kwargs)
