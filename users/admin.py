# admin.py
from django.contrib import admin
from users.forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    """
    Custom admin interface for managing User models.
    
    Configures the Django admin interface to properly handle the custom user model
    with email authentication and additional name fields.
    """
    model = User 
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ['first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser', 'date_joined']
    list_filter = ['is_staff', 'is_active', 'is_superuser']
    fieldsets = (
        (
            _("Login credentials"),
            {"fields": ("email", "password")},
        ),
        (
            _("Personal Info"),
            {"fields": ("first_name", "last_name")},
        ),
        (
            _("Permissions and Groups"),
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        (
            _("Important Dates"),
            {"fields": ("date_joined",)}
        ),
    )
    search_fields = ["email", "username"]
    ordering = ["email"]