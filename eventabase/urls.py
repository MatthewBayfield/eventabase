"""eventabase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from allauth.account import views

urlpatterns = [
    path('', include('landing_page.urls')),
    path('accounts/', include('allauth.urls')),
    re_path(r"^accounts/password/reset/key/(?P<uidb36>.+)-(?P<key>.+)/$",
            views.password_reset_from_key,
            name="account_reset_password_from_key"),
    path('home/', include('home.urls')),
    path('events_and_activities/', include('events_and_activities.urls')),
    path('admin/', admin.site.urls)
]
