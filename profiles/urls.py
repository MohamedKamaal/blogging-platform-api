from django.urls import path 
from profiles.views import ProfileRetrieveAPIView, ProfileListAPIView, FollowAPIView, UnFollowAPIView, FollowersAPIView, FollowingsAPIView
app_name="profiles"

urlpatterns = [
    path("me/",ProfileRetrieveAPIView.as_view(), name="profile"),
    path("all/",ProfileListAPIView.as_view(), name="profiles"),
    path("<uuid:profile_id>/follow/",FollowAPIView.as_view(), name="profile-follow"),
    path("<uuid:profile_id>/unfollow/",UnFollowAPIView.as_view(), name="profile-unfollow"),
    path("me/followings/",FollowingsAPIView.as_view(), name="followings"),
    path("me/followers/",FollowersAPIView.as_view(), name="followers"),
]