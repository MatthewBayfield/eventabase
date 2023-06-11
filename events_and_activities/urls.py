from django.urls import path
from events_and_activities.views import SearchAdvertsView, RetrieveContactInfoView

app_name = 'events_and_activities'
urlpatterns = [
    path('search_event_adverts/', SearchAdvertsView.as_view(extra_context={'page_id': 'search_adverts',
                                                                           'logged_in': True}),
         name='search_adverts_page'),
    path('retrieve_contact_info/', RetrieveContactInfoView.as_view(), name='retrieve_contact_info')
]
