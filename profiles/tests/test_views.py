import pytest
from rest_framework import status
from rest_framework.test import APIClient
from profiles.models import Profile
from profiles.factories import UserFactory, ProfileFactory

from django.urls import reverse
from rest_framework import status

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_retrieve_own_profile(api_client):
    user = UserFactory()
    
    api_client.force_authenticate(user=user)

    url = reverse("profiles:profile")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == user.email

@pytest.mark.django_db
def test_list_all_profiles(api_client):
    user = UserFactory()

    api_client.force_authenticate(user=user)
    url = reverse("profiles:profiles")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) >= 1  # assuming at least one profile

@pytest.mark.django_db
def test_follow_another_user(api_client):
    user1 = UserFactory()
    user2 = UserFactory()
    profile1 = user1.profile
    profile2 = user2.profile
    api_client.force_authenticate(user=user1)
    url = reverse("profiles:profile-follow", kwargs={"profile_id": profile2.id})
    response = api_client.post(url)

    assert response.status_code == 200
    assert "You are now following" in response.data["message"]

@pytest.mark.django_db
def test_cannot_follow_yourself(api_client):
    user = UserFactory()
    profile = user.profile
    api_client.force_authenticate(user=user)

    url = reverse("profiles:profile-follow", kwargs={"profile_id": profile.id})
    response = api_client.post(url)

    assert response.status_code == 403 

@pytest.mark.django_db
def test_unfollow_user(api_client):
    user1 = UserFactory()
    user2 = UserFactory()
    profile1 = user1.profile
    profile2 = user2.profile
    profile1.follow(profile2)

    api_client.force_authenticate(user=user1)
    url = reverse("profiles:profile-unfollow", kwargs={"profile_id": profile2.id})
    response = api_client.post(url)

    assert response.status_code == 200
    assert "unfollowing" in response.data["message"]

@pytest.mark.django_db
def test_get_followers(api_client):
    user1 = UserFactory()
    user2 = UserFactory()
    profile1 = user1.profile
    profile2 = user2.profile
    profile2.follow(profile1)

    api_client.force_authenticate(user=user1)
    url = reverse("profiles:followers")
    response = api_client.get(url)

    assert response.status_code == 200
    assert any(f["email"] == user2.email for f in response.data)

@pytest.mark.django_db
def test_get_followings(api_client):
    user1 = UserFactory()
    user2 = UserFactory()
    profile1 = user1.profile
    profile2 = user2.profile
    profile1.follow(profile2)

    api_client.force_authenticate(user=user1)
    url = reverse("profiles:followings")
    response = api_client.get(url)

    assert response.status_code == 200
    assert any(f["email"] == user2.email for f in response.data)
