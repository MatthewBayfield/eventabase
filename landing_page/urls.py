from django.urls import path
from . import views

app_name = 'landing_page'
urlpatterns = [
    path('', views.LandingPage.as_view(extra_context={'slogan': 'Events & Activities Organised by You for You', 'page_id': 'landing_page'}), name='landing_page_url')
]
