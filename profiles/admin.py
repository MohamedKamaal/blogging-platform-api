# admin.py
from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    """
    Custom admin interface for managing Profile models in the Django admin panel.

    Attributes:
        list_display (tuple): Fields to display in the list view of the admin panel.
        search_fields (tuple): Fields that can be searched in the admin panel.
        list_filter (tuple): Fields that can be used to filter results in the admin panel.
    """

    list_display = ('user', 'bio', 'gender', 'phone_number', 'country', 'city', 'profile_pic')  # Customize fields as needed
    search_fields = ('user__username', 'bio', 'country')  # Add search functionality
    list_filter = ('country', 'city')  # Add filters


admin.site.register(Profile, ProfileAdmin)