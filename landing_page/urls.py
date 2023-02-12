from django.urls import path
from . import views

app_name = 'landing_page'
urlpatterns = [
    path('', views.LandingPage.as_view(extra_context={'slogan': 'Events & Activities Organised by You for You',
                                                      'page_id': 'landing_page',
                                                      'logged_in': False}), name='landing_page_url'),
    path('terms_and_policies/', views.TermsPoliciesView.as_view(extra_context={'page_id': 'T_and_c'}), name='terms_view')
]
