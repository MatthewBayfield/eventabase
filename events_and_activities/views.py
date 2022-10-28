from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.template.loader import get_template
from allauth.account.decorators import verified_email_required
# from .models import UserProfile, UserAddress

# Create your views here.

@method_decorator(verified_email_required, name='dispatch')
class PostEventsView(FormView):
    """
    """
    post_events_section_template = get_template('events_and_activities/post_section.html')
    
    # def __init__(self, **kwargs):
    #     """
    #     Calls the TemplateView constructor. Sets initial context.
    #     """
    #     super().__init__(**kwargs)
    #     self.further_context = {}

    def get(self, request, *args, **kwargs):
        """
        Handles GET request for rendered events_template
        """
        if request.path != reverse('home:user_homepage'):
            return redirect(reverse('home:user_homepage'))
            
        rendered_post_events_section_template = self.post_events_section_template.render()
        return rendered_post_events_section_template
