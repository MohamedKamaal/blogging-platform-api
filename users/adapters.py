# users/adapters.py
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom account adapter that extends DefaultAccountAdapter to handle user saving
    with additional fields (first_name, last_name) during registration.
    """

    def save_user(self, request, user, form, commit=True):
        """
        Saves a new user instance with additional fields from the registration form.

        Args:
            request: HttpRequest object
            user: User model instance
            form: Registration form instance
            commit (bool): Whether to save the user to database immediately

        Returns:
            tuple: (user, created) - user instance and boolean indicating if user was created
        """
        user = super().save_user(request, user, form, commit=False)
        user.email = form.cleaned_data.get('email')
        user.first_name = form.cleaned_data.get('first_name')
        user.last_name = form.cleaned_data.get('last_name')
        user.set_password(form.cleaned_data.get('password1'))
        
        if commit:
            user.save()
        return user