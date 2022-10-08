from django.views.generic.base import TemplateView

# Create your views here.


class UserHomePage(TemplateView):
    """
    View for the user home page.
    """
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context