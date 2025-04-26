# factories.py
import factory
from django.contrib.auth import get_user_model
from cities_light.models import Country, City
from phonenumber_field.phonenumber import PhoneNumber
from profiles.models import Profile
from users.factories import UserFactory

User = get_user_model()


class ProfileFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating test Profile instances.

    This factory creates Profile objects with realistic dummy data for testing purposes.
    It automatically creates a related User instance through the UserFactory.

    Attributes:
        user: Related User instance created via UserFactory
        profile_pic: Generated dummy image file
        bio: Randomly generated text for biography
        gender: Default gender value ('M')
    """

    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    profile_pic = factory.django.ImageField(filename="profile.jpg")
    bio = factory.Faker("text", max_nb_chars=200)
    gender = 'M'