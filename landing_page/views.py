from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.


class LandingPage(TemplateView):
    """
    View that serves the landing_page template
    """
    template_name = "landing_page/landing_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
