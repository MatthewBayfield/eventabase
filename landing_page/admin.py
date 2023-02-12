from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . models import CustomUserModel

# Register your models here.


class CustomUserAdmin(UserAdmin):
    """
    Custom User admin class
    """
    description = 'If creating a new user, remember to also create a new email address model instance.'

    fieldsets = (
                (None, {"fields": ("email", "username", "password")}),
                ("Permissions", {"fields": (
                                            "is_active", "is_staff",
                                            "is_superuser",
                                            "groups",
                                            "user_permissions")}),
                ("Important dates", {"fields": ("last_login", "date_joined")}))

    add_fieldsets = ((None, {"classes": ("wide",),
                             "fields": ("email", "username",
                                        "password1", "password2"),
                             "description": description}),)

    list_display = ("username", "email", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "email")


admin.site.register(CustomUserModel, CustomUserAdmin)
