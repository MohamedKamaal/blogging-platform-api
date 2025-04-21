from django.shortcuts import get_object_or_404
from profiles.serializers import ProfileOutSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from profiles.models import Profile
from profiles.exceptions import CantFollowYourself
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class ProfileRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    def get_object(self):
        profile = self.request.user.profile
        return profile
    serializer_class = ProfileOutSerializer


class ProfileListAPIView(ListAPIView):
    queryset = Profile.objects.select_related("user")
    serializer_class = ProfileOutSerializer
    permission_classes = [IsAuthenticated]


class FollowAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, profile_pkid ,*args, **kwargs):
        own_profile = request.user.profile
        profile = get_object_or_404(Profile, pkid=profile_pkid)
        if own_profile.pkid == profile_pkid:
            raise CantFollowYourself
        if own_profile.is_following(profile):
            return Response({"message":f"You are already following {profile.user.fullname}"},status=403)
        own_profile.follow(profile)
        return Response({"message":f"You are now following {profile.user.fullname}"},status=200)
        
class UnFollowAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, profile_pkid ,*args, **kwargs):
        own_profile = request.user.profile
        profile = get_object_or_404(Profile, pkid=profile_pkid)
        if own_profile.pkid == profile_pkid:
            raise CantFollowYourself
        if own_profile.is_following(profile):
            own_profile.unfollow(profile)
            return Response({"message":f"You are now unfollowing {profile.user.fullname}"},status=200)
        return Response(
            {"message": f"You can't unfollow {profile.user.fullname} because you weren't following them in the first place"},
            status=status.HTTP_403_FORBIDDEN,
        )

class FollowersAPIView(ListAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileOutSerializer

    def get_queryset(self):
        profile = self.request.user.profile 
        followers = profile.followers.select_related("user")
        return followers
    
class FollowingsAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileOutSerializer

    def get_queryset(self):
        profile = self.request.user.profile 
        following = profile.following.select_related("user")
        return following
    