from django.urls import reverse
from django.views.generic.base import TemplateView
from django.shortcuts import redirect

# Create your views here.


class LandingPage(TemplateView):
    """
    View that serves the landing_page template
    """
    template_name = "landing_page/landing_page.html"

    def get(self, request, *args, **kwargs):
        """
        Handles GET request
        """
        if request.user.is_authenticated:
            return redirect(reverse('home:user_homepage'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Returns template context
        """
        context = super().get_context_data(**kwargs)
        return context


class TermsPoliciesView(TemplateView):
    """
    View that serves the terms and conditions template
    """
    template_name = "landing_page/terms_and_conditions.html"

    def __init__(self, **kwargs):
        self.logged_in = False

    def get(self, request, *args, **kwargs):
        """
        Handles GET request
        """
        if request.user.is_authenticated:
            self.logged_in = True
        kwargs.update({'logged_in': self.logged_in})
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Returns template context
        """
        context = super().get_context_data(**kwargs)
        return context
