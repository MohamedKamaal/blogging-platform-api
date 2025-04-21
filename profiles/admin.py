# admin.py
from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'gender', 'phone_number','country','city','profile_pic')  # Customize fields as needed
    search_fields = ('user__username', 'bio', 'country')  # Add search functionality
    list_filter = ('country','city')  # Add filters

admin.site.register(Profile, ProfileAdmin)