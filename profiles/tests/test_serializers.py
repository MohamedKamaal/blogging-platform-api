import pytest
from rest_framework.exceptions import ValidationError
from profiles.models import Profile
from profiles.factories import ProfileFactory, UserFactory
from profiles.serializers import ProfileOutSerializer
from cities_light.models import Country, City


@pytest.mark.django_db
class TestProfileOutSerializer:
    
   
    def test_profile_out_serializer(self):

        """Test that the ProfileOutSerializer correctly serializes the profile data."""
        user = UserFactory()
        profile = user.profile
        serializer = ProfileOutSerializer(profile)

        # Check that all required fields are serialized
        assert serializer.data['email'] == profile.user.email
        assert serializer.data['first_name'] == profile.user.first_name
        assert serializer.data['last_name'] == profile.user.last_name
      

    
   