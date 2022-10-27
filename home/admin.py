from django.contrib import admin
from .models import UserAddress, UserProfile

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    """
    pass

@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    """
    """
    pass