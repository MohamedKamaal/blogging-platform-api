from django.db import models
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from cities_light.models import Country, City
from django.utils.translation import gettext as _

from common.models import TimeStampedModel

User = get_user_model()


class Profile(TimeStampedModel):
    """User profile model extending the base User model with additional personal information.
    
    Inherits from TimeStampedModel for automatic creation/update timestamps.
    Provides extended user information including location, bio, gender, and social features.
    
    Attributes:
        user (OneToOneField): Link to the associated User account
        country (ForeignKey): User's country of residence
        city (ForeignKey): User's city of residence
        profile_pic (ImageField): User's profile picture
        bio (TextField): Short biography/about text
        gender (CharField): User's gender (M/F)
        phone_number (PhoneNumberField): User's phone number
        followers (ManyToManyField): Users who follow this profile
    """
    
    class Gender(models.TextChoices):
        """Gender choices for user profiles."""
        MALE = "m", _("Male")
        FEMALE = "f", _("Female")

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    profile_pic = models.ImageField(
        _("Profile picture"), 
        help_text=_("Upload your profile picture"),
        null=True,
        blank=True
    )
    bio = models.TextField(
        _("User bio"),
        help_text=_("Tell us about yourself"),
        null=True,
        blank=True
    )
    gender = models.CharField(
        _("User Gender"),
        help_text=_("Gender"),
        max_length=1,
        null=True,
        blank=True,
        choices=Gender.choices
    )
    phone_number = PhoneNumberField(
        _("Phone number"),
        help_text=_("Enter phone number with country code"),
        unique=True,
        null=True,
        blank=True
    )
    followers = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="following"
    )

    def follow(self, profile):
        """Add a follow relationship to another profile.
        
        Args:
            profile (Profile): The profile to follow
        """
        self.following.add(profile)

    def unfollow(self, profile):
        """Remove a follow relationship with another profile.
        
        Args:
            profile (Profile): The profile to unfollow
        """
        self.following.remove(profile)

    def is_following(self, profile):
        """Check if this profile is following another profile.
        
        Args:
            profile (Profile): The profile to check
            
        Returns:
            bool: True if following, False otherwise
        """
        return self.following.filter(pkid=profile.pkid).exists()

    def __str__(self):
        """String representation of the profile (user's full name)."""
        return f"{self.user.full_name}"