import factory
from django.contrib.auth import get_user_model
from cities_light.models import Country,City
from phonenumber_field.phonenumber import PhoneNumber
from profiles.models import Profile
from users.factories import UserFactory
User = get_user_model()


class CountryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Country

    name = factory.Faker("country")

class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = City

    name = factory.Faker("city")
    country = factory.SubFactory(CountryFactory)

class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    country = factory.SubFactory(CountryFactory)
    city = factory.SubFactory(CityFactory)
    profile_pic = factory.django.ImageField(filename="profile.jpg")
    bio = factory.Faker("text", max_nb_chars=200)
    gender = Profile.Gender.M
    phone_number = PhoneNumber("+12025550123")
