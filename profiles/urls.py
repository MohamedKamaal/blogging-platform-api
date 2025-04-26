# urls.py
from django.urls import path
from profiles.views import (
    ProfileRetrieveAPIView,
    ProfileListAPIView,
    FollowAPIView,
    UnFollowAPIView,
    FollowersAPIView,
    FollowingsAPIView
)

app_name = "profiles"

urlpatterns = [
    # Endpoint to retrieve the current user's profile
    path("me/", ProfileRetrieveAPIView.as_view(), name="profile"),
    
    # Endpoint to list all profiles
    path("all/", ProfileListAPIView.as_view(), name="profiles"),
    
    # Endpoint to follow a specific profile
    path("<uuid:profile_id>/follow/", FollowAPIView.as_view(), name="profile-follow"),
    
    # Endpoint to unfollow a specific profile
    path("<uuid:profile_id>/unfollow/", UnFollowAPIView.as_view(), name="profile-unfollow"),
    
    # Endpoint to list profiles the current user is following
    path("me/followings/", FollowingsAPIView.as_view(), name="followings"),
    
    # Endpoint to list profiles following the current user
    path("me/followers/", FollowersAPIView.as_view(), name="followers"),
]