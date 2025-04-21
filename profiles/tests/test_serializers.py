import pytest
from rest_framework.exceptions import ValidationError
from profiles.models import Profile
from profiles.factories import ProfileFactory, UserFactory
from profiles.serializers import ProfileOutSerializer
from cities_light.models import Country, City


@pytest.mark.django_db
class TestProfileOutSerializer:
    
    @pytest.fixture
    def user(self):
        return UserFactory()

    @pytest.fixture
    def profile(self, user):
        return ProfileFactory(user=user)

    def test_profile_out_serializer(self, profile):
        """Test that the ProfileOutSerializer correctly serializes the profile data."""
        serializer = ProfileOutSerializer(profile)

        # Check that all required fields are serialized
        assert serializer.data['email'] == profile.user.email
        assert serializer.data['first_name'] == profile.user.first_name
        assert serializer.data['last_name'] == profile.user.last_name
        assert serializer.data['bio'] == profile.bio
        assert serializer.data['country'] == profile.country.name
        assert serializer.data['city'] == profile.city.name
        assert 'profile_pic' in serializer.data
        assert 'phone_number' in serializer.data

    def test_profile_out_serializer_invalid_country_city(self):
        """Test that the serializer raises a validation error when the city is not in the selected country."""
        country = Country.objects.create(name="Test Country", code="TC")
        city = City.objects.create(name="Test City", country=country)

        # Creating a valid Profile
        user = UserFactory()
        profile = ProfileFactory(user=user, country=country, city=city)

        # Now create an invalid scenario where the city is not in the same country
        other_country = Country.objects.create(name="Other Country", code="OC")
        invalid_profile_data = {
            'bio': 'This is a bio.',
            'country': other_country.name,  # different country
            'city': city.name,  # same city but different country
            'gender': 'm',
        }

        serializer = ProfileOutSerializer(data=invalid_profile_data)
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_valid_serializer_data(self):
        """Test that the serializer validates correctly with valid data."""
        user = UserFactory()
        profile_data = {
            'bio': 'This is a bio.',
            'country': 'Test Country',  # Assume this country is already created
            'city': 'Test City',        # Assume this city is already created
            'gender': 'm',
        }
        serializer = ProfileOutSerializer(data=profile_data)
        assert serializer.is_valid()
        assert serializer.validated_data['bio'] == 'This is a bio.'
        assert serializer.validated_data['country'] == 'Test Country'
        assert serializer.validated_data['city'] == 'Test City'

    def test_invalid_city_country_combination(self):
        """Test that the serializer raises a validation error if the city is not in the chosen country."""
        country = Country.objects.create(name="Country 1", code="C1")
        other_country = Country.objects.create(name="Country 2", code="C2")
        city = City.objects.create(name="City 1", country=country)
        
        # Now try to create a profile with a city in a different country
        profile_data = {
            'bio': 'This is a bio.',
            'country': other_country.name,  # Different country
            'city': city.name,              # City in another country
            'gender': 'm',
        }
        serializer = ProfileOutSerializer(data=profile_data)
        assert not serializer.is_valid()
        assert 'city' in serializer.errors
        assert serializer.errors['city'] == ["Selected city is not in the chosen country."]
