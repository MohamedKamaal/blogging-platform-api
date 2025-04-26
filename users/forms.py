# forms.py
from django.contrib.auth import get_user_model
from django import forms 
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """
    Custom user creation form that validates email uniqueness.
    
    Extends UserCreationForm to use email as primary identifier and adds
    validation for duplicate email addresses.
    """
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "is_active", "is_staff", "is_superuser"]
    
    def clean_email(self):
        """
        Validates that the email address is not already in use.
        
        Returns:
            str: The validated email address
            
        Raises:
            ValidationError: If email is already registered
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already taken")
        return email


class CustomUserChangeForm(UserChangeForm):
    """
    Custom user change form that validates email uniqueness.
    
    Extends UserChangeForm to validate email uniqueness when updating user information.
    """
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "is_active", "is_staff", "is_superuser"]
    
    def clean_email(self):
        """
        Validates that the email address is not already in use by another user.
        
        Returns:
            str: The validated email address
            
        Raises:
            ValidationError: If email is already registered to another user
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already taken")
        return email