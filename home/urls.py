from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.UserHomePage.as_view(extra_context={'page_id': 'home_page'}), name='user_homepage')
]