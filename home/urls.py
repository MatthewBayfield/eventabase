from django.urls import path
from events_and_activities.views import PostEventsView, UpdateEventsView, ViewEventsView
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.UserHomePage.as_view(extra_context={'page_id': 'home_page',
                                                       'logged_in': True}),
         name='user_homepage'),
    path('profile_form/', views.ProfileFormView.as_view(),
         name='profile_form_view'),
    path('post_events/', PostEventsView.as_view(), name='post_events_view'),
    path('update_events/', UpdateEventsView.as_view(), name='update_events_view'),
    path('event_withdrawal/', ViewEventsView.as_view(), name='view_events_view')
]
