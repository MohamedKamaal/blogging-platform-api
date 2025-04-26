# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

User = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
    """
    Custom registration serializer that removes username field and adds first/last name.
    
    Extends the default RegisterSerializer to support email-only registration with
    additional required name fields.
    """
    username = None  # Remove the username field
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def get_cleaned_data(self):
        """
        Extends parent method to include first_name and last_name in cleaned data.
        
        Returns:
            dict: Dictionary of validated registration data
        """
        data = super().get_cleaned_data()
        data.update({
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
        })
        return data

    def save(self, request):
        """
        Creates a new user instance with the validated registration data.
        
        Args:
            request: HttpRequest object
            
        Returns:
            User: The newly created user instance
        """
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)

        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.email = self.cleaned_data.get("email")
        user.set_password(self.cleaned_data.get("password1"))
        user.save()
        setup_user_email(request, user, [])
        return user