from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext as _
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

# Create your models here.

class CustomUserManager(BaseUserManager):
    """ custom user manager """

    def create_user(self, email, password, first_name, last_name, **kwargs):
        if not email:
            raise ValueError(_("email nust be set"))
        
        if not first_name:
            raise ValueError(_("first name nust be set"))
        
        if not last_name:
            raise ValueError(_("last name nust be set"))
        
        # validate email 
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Email is not valid")
        
        # normalize email 
        email = self.normalize_email(email=email)
        
        # save model 
        user = self.model(email=email,first_name=first_name, last_name=last_name, **kwargs)

        user.set_password(password)
        
        user.save(using=self._db)
        
        return user

    def create_superuser(self, email, password, first_name, last_name, **kwargs):
        kwargs.setdefault("is_active",True)
        kwargs.setdefault("is_superuser",True)
        kwargs.setdefault("is_staff",True)

        user = self.create_user(email, password, first_name, last_name, **kwargs)

        return user



class CustomUser(AbstractBaseUser,PermissionsMixin):
    first_name = models.CharField(verbose_name=_("First Name"),max_length=110)
    last_name = models.CharField(verbose_name=_("Last Name"),max_length=110)
    email = models.EmailField(_("Email Field"), unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = "email"
    
    REQUIRED_FIELDS = ["first_name","last_name"]
    
    
    def get_by_natural_key(self, email):
        return self.get(email=email)
    
    def __str__(self):
        return str(self.email)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
        
