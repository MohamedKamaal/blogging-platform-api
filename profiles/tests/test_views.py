import pytest
from rest_framework import status
from rest_framework.test import APIClient
from profiles.models import Profile
from profiles.factories import UserFactory, ProfileFactory

@pytest.mark.django_db
class TestProfileViews:

    @pytest.fixture
    def user(self):
        return UserFactory()

    @pytest.fixture
    def profile(self, user):
        return ProfileFactory(user=user)

    @pytest.fixture
    def client(self, user):
        client = APIClient()
        client.force_authenticate(user=user)
        return client

    def test_profile_retrieve(self, client, profile):
        """Test retrieving the profile of the authenticated user."""
        url = '/profiles/me/'
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == profile.user.email
        assert response.data['first_name'] == profile.user.first_name
        assert response.data['last_name'] == profile.user.last_name

    def test_profile_update(self, client, profile):
        """Test updating the profile of the authenticated user."""
        url = '/profiles/me/'
        data = {
            'bio': 'Updated bio.',
            'country': profile.country.name,
            'city': profile.city.name,
            'gender': 'm'
        }
        response = client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['bio'] == 'Updated bio.'

    def test_profile_list(self, client, profile):
        """Test listing all profiles."""
        url = '/profiles/profiles/'
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'email' in response.data[0]

    def test_follow_user(self, client, profile):
        """Test following another user."""
        other_user = UserFactory()
        other_profile = ProfileFactory(user=other_user)
        
        url = f'/profiles/{other_profile.pkid}/follow/'
        response = client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data
        assert response.data['message'] == f"You are now following {other_user.first_name} {other_user.last_name}"

    def test_follow_self(self, client, profile):
        """Test following oneself raises an error."""
        url = f'/profiles/{profile.pkid}/follow/'
        response = client.post(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'message' in response.data
        assert response.data['message'] == "You cannot follow yourself."

    def test_unfollow_user(self, client, profile):
        """Test unfollowing a user."""
        other_user = UserFactory()
        other_profile = ProfileFactory(user=other_user)
        profile.follow(other_profile)

        url = f'/profiles/{other_profile.pkid}/unfollow/'
        response = client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data
        assert response.data['message'] == f"You are now unfollowing {other_user.first_name} {other_user.last_name}"

    def test_followings_list(self, client, profile):
        """Test listing the profiles the user is following."""
        other_user = UserFactory()
        other_profile = ProfileFactory(user=other_user)
        profile.follow(other_profile)

        url = '/profiles/followings/'
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['email'] == other_user.email

    def test_followers_list(self, client, profile):
        """Test listing the followers of the user."""
        other_user = UserFactory()
        other_profile = ProfileFactory(user=other_user)
        other_profile.follow(profile)

        url = '/profiles/followers/'
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['email'] == other_user.email
