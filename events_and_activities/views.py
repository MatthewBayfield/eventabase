from django.views.generic.edit import FormView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.template.loader import get_template
from allauth.account.decorators import verified_email_required
from .models import EventsActivities
from .forms import EventsActivitiesForm

# Create your views here.

@method_decorator(verified_email_required, name='dispatch')
class PostEventsView(FormView):
    """
    """
    post_events_section_template = get_template('events_and_activities/post_section.html')
    post_events_modal_template = get_template('events_and_activities/post_events_modal.html')
    
    def __init__(self, **kwargs):
        """
        Calls the TemplateView constructor. Sets initial context.
        """
        super().__init__(**kwargs)
        self.further_context = {}
        self.form_class = EventsActivitiesForm

    def get(self, request, *args, **kwargs):
        """
        Handles GET request for rendered events_template
        """
        if request.path != reverse('home:user_homepage'):
            return redirect(reverse('home:user_homepage'))

        if not kwargs['get_modal']:
            EventsActivities.expired.delete_expired(request.user)
            EventsActivities.expired.update_expired(request.user)
            all_posted_events_for_user = EventsActivities.objects.filter(host_user=request.user)
            all_advertsied_events_for_user = all_posted_events_for_user.filter(status='advertised')
            all_upcoming_events_for_user = all_posted_events_for_user.filter(status='confirmed')

            all_advertised_hosting_events_data = []
            for event in all_advertsied_events_for_user:
                data = event.retrieve_field_data()
                data.pop('status')
                data['closing date'] = data['closing date'].strftime("%H:%M, %d/%m/%y")
                data['when'] = data['when'].strftime("%H:%M, %d/%m/%y")
                all_advertised_hosting_events_data.append(data)

            all_upcoming_hosting_events_data = []
            for event in all_upcoming_events_for_user:
                data = event.retrieve_field_data()
                data.pop('status')
                data['closing date'] = data['closing date'].strftime("%H:%M, %d/%m/%y")
                data['when'] = data['when'].strftime("%H:%M, %d/%m/%y")
                all_upcoming_hosting_events_data.append(data)

            kwargs.update({'upcoming_hosting_events_data': all_upcoming_hosting_events_data,
                           'advertised_hosting_events_data': all_advertised_hosting_events_data})
            rendered_post_events_section_template = self.post_events_section_template.render(kwargs, request)
            return rendered_post_events_section_template

        post_events_form = self.get_form()
        kwargs.update({'post_events_form': post_events_form})
        rendered_post_events_modal_template = self.post_events_modal_template.render(kwargs, request)
        return rendered_post_events_modal_template
