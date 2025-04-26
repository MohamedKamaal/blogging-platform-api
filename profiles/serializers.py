from rest_framework import serializers
from django.contrib.auth import get_user_model
from profiles.models import Profile 
from django_countries.serializers import CountryFieldMixin
from cities_light.models import City, Country

User = get_user_model()


class ProfileOutSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """Serializer for outputting complete profile data including related user information.
    
    Inherits from CountryFieldMixin for proper country field serialization.
    Includes validation to ensure city-country consistency.
    
    Fields:
        country (SlugRelatedField): Country name (slug-related)
        city (SlugRelatedField): City name (slug-related)
        phone_number: User's phone number
        profile_pic: URL to profile picture
        gender: User's gender
        bio: User's biography text
        email (ReadOnlyField): User's email from related User model
        first_name (ReadOnlyField): User's first name from related User model
        last_name (ReadOnlyField): User's last name from related User model
    
    Validation:
        - Ensures selected city belongs to selected country
    """
    
    country = serializers.SlugRelatedField(
        queryset=Country.objects.all(),
        slug_field='name'
    )
    city = serializers.SlugRelatedField(
        queryset=City.objects.all(),
        slug_field='name'
    )
    email = serializers.ReadOnlyField(source="user.email")
    first_name = serializers.ReadOnlyField(source="user.first_name")
    last_name = serializers.ReadOnlyField(source="user.last_name")

    class Meta:
        model = Profile
        fields = [
            'country', 'city', 'phone_number', 'profile_pic',
            'gender', 'bio', 'email', 'first_name', 'last_name'
        ]
    
    def validate(self, attrs):
        """Validate that the selected city belongs to the selected country.
        
        Args:
            attrs (dict): Dictionary of attribute values
            
        Returns:
            dict: Validated attributes if validation passes
            
        Raises:
            ValidationError: If city doesn't belong to selected country
        """
        data = attrs
        city = data.get("city")
        country = data.get("country")
        
        if city and country and city.country == country.name:
            return data
        raise serializers.ValidationError(
            {"city": "Selected city is not in the chosen country."}
        )