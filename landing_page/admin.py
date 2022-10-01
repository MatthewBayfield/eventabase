from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . models import CustomUserModel

# Register your models here.


class CustomUserAdmin(UserAdmin):
    """
    Custom User admin class
    """
    fieldsets = (
                (None, {"fields": ("email", "username", "password")}),
                ("Permissions", {"fields": (
                                            "is_active", "is_staff",
                                            "is_superuser",
                                            "groups",
                                            "user_permissions")}),
                ("Important dates", {"fields": ("last_login", "date_joined")}))

    add_fieldsets = ((None, {"classes": ("wide",),
                             "fields": ("email1", "email2", "username",
                                        "password1", "password2")}))

    list_display = ("username", "email", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "email")


admin.site.register(CustomUserModel, CustomUserAdmin)
