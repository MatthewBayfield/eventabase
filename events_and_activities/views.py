from django.views.generic.edit import FormView, View
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.template.loader import get_template, render_to_string
from django.views.decorators.csrf import ensure_csrf_cookie
from allauth.account.decorators import verified_email_required
from .models import EventsActivities
from .forms import EventsActivitiesForm

# Create your views here.

@method_decorator([verified_email_required], name='dispatch')
class PostEventsView(FormView):
    """
    Responsible for retrieving and displaying a user's advertised or upcoming events that they are hosting
    in the post events section of their homepage. Also responsible for handling the post events form
    creation and submission.

    Attributes:
        post_events_section_template: template for the post events section of the homepage.
        post_events_modal_template: template for the post events form modal.
        further_context (dict): context dictionary.
        form_class (obj): form class for the post events form.
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
        Handles GET requests for rendered post_section and post_events_modal templates.
        """
        if request.path != reverse('home:user_homepage'):
            # establish whether it is a form refresh request
            if request.environ['QUERY_STRING'] == 'refresh=true':
                kwargs.update({'get_modal': True, 'modal': 'post_events_modal',
                               'button1_name': 'Done', 'button2_name': 'Cancel'})
            else:
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
                data.pop('engagement')
                data.pop('attendees')
                data['closing date'] = data['closing date'].strftime("%H:%M, %d/%m/%y")
                data['when'] = data['when'].strftime("%H:%M, %d/%m/%y")
                all_advertised_hosting_events_data.append(data)

            all_upcoming_hosting_events_data = []
            for event in all_upcoming_events_for_user:
                data = event.retrieve_field_data()
                data.pop('status')
                data.pop('engagement')
                data.pop('attendees')
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
        if request.GET.get('refresh', ''):
            return JsonResponse({'modal': rendered_post_events_modal_template})
        return rendered_post_events_modal_template

    def post(self, request, *args, **kwargs):
        """
        Handles the post events form submission via a fetch request.

        Returns:
            A JSON response with with either the submitted form instance with error feedback, if the submitted form was
            invalid; or a rendered string of the event template with context generated from the newly created event data,
            if the form is valid.
        """
        data = {}

        form_data = request.POST
        form_data = {key: value for key, value in form_data.dict().items() if key != 'csrfmiddlewaretoken'}
        form_data.update({'host_user': request.user})
        new_event_form = EventsActivitiesForm(data=form_data)
        valid = new_event_form.is_valid()
        if valid:
            new_event_form.post_clean_processing()
            new_event = new_event_form.save()
            new_event_data = new_event.retrieve_field_data()
            new_event_data.pop('status')
            new_event_data.pop('engagement')
            new_event_data.pop('attendees')
            new_event_data['closing date'] = new_event_data['closing date'].strftime("%H:%M, %d/%m/%y")
            new_event_data['when'] = new_event_data['when'].strftime("%H:%M, %d/%m/%y")
            rendered_event = render_to_string(template_name='events_and_activities/event.html',
                                              context={'event': new_event_data},
                                              request=request)
            rendered_blank_form = str(EventsActivitiesForm())
            data.update({'event': rendered_event, 'valid': 'true', 'form': rendered_blank_form})
        else:
            rendered_form = render_to_string(template_name='events_and_activities/post_events_form.html', context=new_event_form.get_context(), request=request)
            data.update({'form': rendered_form, 'valid': 'false'})
        return JsonResponse(data)


@method_decorator(verified_email_required, name='dispatch')
class UpdateEventsView(View):
    """
    Responsible for processing requests to delete a host user's existing event advert, as well as cancel one of their
    upcoming events. Updates the EventsActivities model database by deleting the matching event.
    """
    def post(self, request):
        """
        Returns:
            A JSON response indicating whether the request was successful with regard to the event deletion. 
        """
        update_type = 'cancel'
        if request.environ['QUERY_STRING'] == 'cancel=false':
            update_type = 'delete'

        event_id = request.body.decode()

        if update_type == 'cancel':
            pass

        try:
            event = EventsActivities.objects.get(id=int(event_id))
            event.delete()
        except Exception as error:
            print(error)

        if not EventsActivities.objects.filter(id__exact=int(event_id)).exists():
            return JsonResponse({'successful': 'true'})

        return JsonResponse({'successful': 'false'})
