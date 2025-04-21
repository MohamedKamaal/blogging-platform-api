from django.db import models
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from cities_light.models import Country,City


from django.utils.translation import gettext as _
# Create your models here.
from common.models import TimeStampedModel
User = get_user_model()

class Profile(TimeStampedModel):
    class Gender(models.TextChoices):
        M = ("m","Male")
        F = ("f","Female")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)

    profile_pic = models.ImageField(_("Profile picture"),help_text=_("Upload your profile picture"),
                           null=True,blank=True)
    bio = models.TextField(_("User bio"),help_text=_("tell us about yourself"),
                           null=True,blank=True)
    
    gender = models.CharField(_("User Gender"),help_text=_("Gender"),
                           max_length=1, null=True,blank=True, choices=Gender.choices)
    
    phone_number = PhoneNumberField(_("Phone number Field"),help_text=_("Enter Phone number"),
                                    unique=True, null=True,blank=True)
    followers = models.ManyToManyField("self",symmetrical=False, related_name="following")
    
    
    def follow(self,profile):
        
        self.following.add(profile)
        
    def unfollow(self,profile):
        
        self.following.remove(profile)
    
    def is_following(self,profile):
        return self.following.filter(pkid=profile.pkid).exists()
        
    def __str__(self):
        return f"{self.user.full_name}"