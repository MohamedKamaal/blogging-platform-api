# tests/test_models.py

import pytest
from profiles.models import Profile
from profiles.factories import ProfileFactory
from users.factories import UserFactory






pytestmark = pytest.mark.django_db

def test_profile_creation_user_full_name():
    user = UserFactory(first_name="John", last_name="Doe")
    profile = Profile.objects.get(user__first_name="John" , user__last_name="Doe")
    assert str(profile.__str__()) == "John Doe"  # Assuming `__str__` is implemented to return fullname

   

# 3. **Test Follow Method**
def test_follow_method():
    user1 = UserFactory()
    user2 = UserFactory()

    user1.profile.follow(user2.profile)

    # Test if user1.profile follows user2.profile
    assert user1.profile.is_following(user2.profile) is True
    assert user2.profile.is_following(user1.profile) is False  # because it's not symmetrical in the model

# 4. **Test Unfollow Method**
def test_unfollow_method():
    user1 = UserFactory()
    user2 = UserFactory()

    user1.profile.follow(user2.profile)
    user1.profile.unfollow(user2.profile)

    # Test if user1.profile unfollowed user2.profile
    assert user1.profile.is_following(user2.profile) is False
    assert user2.profile.is_following(user1.profile) is False

# 5. **Test is_following Method**
def test_is_following_method():
    user1 = UserFactory()
    user2 = UserFactory()

    assert user1.profile.is_following(user2.profile) is False
    user1.profile.follow(user2.profile)
    assert user1.profile.is_following(user2.profile) is True



# 8. **Test Symmetry of ManyToManyField (Followers)**
def test_following_symmetry():
    user1 = UserFactory()
    user2 = UserFactory()

    user1.profile.follow(user2.profile)
    
    # Test if user1.profile is in user2.profile's followers (should be symmetrical=False)
    assert user2.profile.following.filter(pk=user1.profile.pk).exists() is False

