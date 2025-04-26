# models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext as _
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    """
    Custom user manager for creating and managing CustomUser instances.
    
    Provides methods for creating regular users and superusers with email authentication.
    """
    
    def create_user(self, email, password, first_name, last_name, **kwargs):
        """
        Creates and saves a regular user with the given email and password.
        
        Args:
            email (str): User's email address (required)
            password (str): User's password (required)
            first_name (str): User's first name (required)
            last_name (str): User's last name (required)
            **kwargs: Additional user attributes
            
        Returns:
            CustomUser: The created user instance
            
        Raises:
            ValueError: If required fields are missing
            ValidationError: If email is invalid
        """
        if not email:
            raise ValueError(_("email must be set"))
        
        if not first_name:
            raise ValueError(_("first name must be set"))
        
        if not last_name:
            raise ValueError(_("last name must be set"))
        
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Email is not valid")
        
        email = self.normalize_email(email=email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name, last_name, **kwargs):
        """
        Creates and saves a superuser with the given email and password.
        
        Args:
            email (str): Superuser's email address
            password (str): Superuser's password
            first_name (str): Superuser's first name
            last_name (str): Superuser's last name
            **kwargs: Additional superuser attributes
            
        Returns:
            CustomUser: The created superuser instance
        """
        kwargs.setdefault("is_active", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_staff", True)
        return self.create_user(email, password, first_name, last_name, **kwargs)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that uses email as the primary identifier instead of username.
    
    Attributes:
        first_name (str): User's first name
        last_name (str): User's last name
        email (str): User's unique email address
        is_active (bool): Whether the user account is active
        is_staff (bool): Whether the user has staff permissions
        is_superuser (bool): Whether the user has superuser permissions
        date_joined (datetime): When the user account was created
    """
    first_name = models.CharField(verbose_name=_("First Name"), max_length=110)
    last_name = models.CharField(verbose_name=_("Last Name"), max_length=110)
    email = models.EmailField(_("Email Field"), unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    
    def get_by_natural_key(self, email):
        """
        Retrieve a user instance by email for authentication purposes.
        
        Args:
            email (str): Email address to look up
            
        Returns:
            CustomUser: User instance matching the email
        """
        return self.get(email=email)
    
    def __str__(self):
        """String representation of the user (email address)."""
        return str(self.email)
    
    @property
    def full_name(self):
        """Returns the user's full name (first + last name)."""
        return f"{self.first_name} {self.last_name}"