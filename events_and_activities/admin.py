from django.contrib import admin
from .models import EventsActivities

# Register your models here.

@admin.register(EventsActivities)
class EventsActivitiesAdmin(admin.ModelAdmin):
    """
    """
    pass
