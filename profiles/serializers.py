from rest_framework import serializers
from django.contrib.auth import get_user_model
from profiles.models import Profile 
from django_countries.serializers import CountryFieldMixin
from cities_light.models import City, Country



User = get_user_model()

""" serializer to output profile data plus user data ,
serializer to update profile """




class ProfileOutSerializer(CountryFieldMixin,serializers.ModelSerializer):
    country = serializers.SlugRelatedField(queryset=Country.objects.all(),
                                           slug_field = 'name')
    city = serializers.SlugRelatedField(
        queryset = City.objects.all(),
    slug_field = 'name'
    )
    email = serializers.ReadOnlyField(source="user.email")
    first_name = serializers.ReadOnlyField(source="user.first_name")
    last_name = serializers.ReadOnlyField(source="user.last_name")
    class Meta:
        model = Profile
        fields = ['country','city','phone_number','profile_pic','gender','bio','email','first_name','last_name']
    
    def validate(self, attrs):
        data = attrs
        city = data.get("city")
        country = data.get("country")
        if city and country and city.country==country.name:
            return data 
        else :
            raise serializers.ValidationError({"city": "Selected city is not in the chosen country."})