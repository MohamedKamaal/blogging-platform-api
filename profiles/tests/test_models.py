import pytest
from profiles.models import Profile
from profiles.factories import ProfileFactory, UserFactory
from cities_light.models import Country, City

@pytest.mark.django_db
class TestProfileModel:
    
    @pytest.fixture
    def user(self):
        return UserFactory()

    @pytest.fixture
    def profile(self, user):
        return ProfileFactory(user=user)

    def test_profile_creation(self, profile):
        """Test that a Profile can be created with valid data."""
        assert profile.user == profile.user
        assert profile.country is not None
        assert profile.city is not None
        assert profile.gender is not None
        assert profile.phone_number is not None

    def test_follow_and_unfollow(self, profile):
        """Test the follow and unfollow functionality."""
        user2 = UserFactory()
        profile2 = ProfileFactory(user=user2)

        # Profile follows another profile
        assert profile.is_following(profile2) is False
        profile.follow(profile2)
        assert profile.is_following(profile2) is True

        # Profile unfollows another profile
        profile.unfollow(profile2)
        assert profile.is_following(profile2) is False

    def test_is_following(self, profile):
        """Test the is_following method."""
        user2 = UserFactory()
        profile2 = ProfileFactory(user=user2)

        assert profile.is_following(profile2) is False

        # Follow user2
        profile.follow(profile2)
        assert profile.is_following(profile2) is True

    def test_follow_cannot_follow_self(self, profile):
        """Test that a profile cannot follow itself."""
        with pytest.raises(CantFollowYourself):
            profile.follow(profile)

    def test_profile_str(self, profile):
        """Test the __str__ method."""
        assert str(profile) == f"{profile.user.fullname}"

    def test_profile_followers(self, profile):
        """Test the followers relationship."""
        user2 = UserFactory()
        profile2 = ProfileFactory(user=user2)

        assert profile.followers.count() == 0
        profile.follow(profile2)
        assert profile.followers.count() == 1

    def test_profile_following(self, profile):
        """Test the following relationship."""
        user2 = UserFactory()
        profile2 = ProfileFactory(user=user2)

        assert profile.following.count() == 0
        profile.follow(profile2)
        assert profile.following.count() == 1
