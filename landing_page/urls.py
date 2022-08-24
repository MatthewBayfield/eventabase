from django.urls import path
from . import views

app_name = 'landing_page'
urlpatterns = [
    path('', views.landing_page.as_view(extra_context={'slogan': 'Events & Activities Organised by You for You'}), name='landing_page_url')
]
