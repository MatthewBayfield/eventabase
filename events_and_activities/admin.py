from django.contrib import admin
from .models import EventsActivities, Engagement

# Register your models here.

@admin.register(EventsActivities)
class EventsActivitiesAdmin(admin.ModelAdmin):
    """
    """

@admin.register(Engagement)
class EngagementAdmin(admin.ModelAdmin):
    """
    """
