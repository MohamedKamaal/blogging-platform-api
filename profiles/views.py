from django.shortcuts import get_object_or_404
from profiles.serializers import ProfileOutSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from profiles.models import Profile
from profiles.exceptions import CantFollowYourself
from rest_framework.response import Response
from rest_framework import status


class ProfileRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    """API endpoint for retrieving, updating and deleting the authenticated user's profile.
    
    Provides:
    - GET: Retrieve current user's profile
    - PUT/PATCH: Update current user's profile
    - DELETE: Delete current user's profile
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileOutSerializer

    def get_object(self):
        """Returns the profile of the currently authenticated user."""
        return self.request.user.profile


class ProfileListAPIView(ListAPIView):
    """API endpoint for listing all user profiles.
    
    Provides:
    - GET: List all profiles in the system
    """
    queryset = Profile.objects.select_related("user")
    serializer_class = ProfileOutSerializer
    permission_classes = [IsAuthenticated]


class FollowAPIView(GenericAPIView):
    """API endpoint for following another user's profile.
    
    POST /profiles/<profile_id>/follow/
    - Creates a follow relationship between current user and target profile
    - Prevents self-following
    - Prevents duplicate follows
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, profile_id, *args, **kwargs):
        """Handle follow request."""
        own_profile = request.user.profile
        profile = get_object_or_404(Profile, id=profile_id)
        
        if own_profile.id == profile_id:
            raise CantFollowYourself
            
        if own_profile.is_following(profile):
            return Response(
                {"message": f"You are already following {profile.user.full_name}"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        own_profile.follow(profile)
        return Response(
            {"message": f"You are now following {profile.user.full_name}"},
            status=status.HTTP_200_OK
        )


class UnFollowAPIView(GenericAPIView):
    """API endpoint for unfollowing a user's profile.
    
    POST /profiles/<profile_id>/unfollow/
    - Removes follow relationship between current user and target profile
    - Prevents self-unfollowing
    - Handles case when not following
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, profile_id, *args, **kwargs):
        """Handle unfollow request."""
        own_profile = request.user.profile
        profile = get_object_or_404(Profile, id=profile_id)
        
        if own_profile.id == profile_id:
            raise CantFollowYourself
            
        if own_profile.is_following(profile):
            own_profile.unfollow(profile)
            return Response(
                {"message": f"You are now unfollowing {profile.user.full_name}"},
                status=status.HTTP_200_OK
            )
            
        return Response(
            {
                "message": (
                    f"You can't unfollow {profile.user.full_name} "
                    "because you weren't following them in the first place"
                )
            },
            status=status.HTTP_403_FORBIDDEN,
        )


class FollowersAPIView(ListAPIView):
    """API endpoint for listing a user's followers.
    
    GET /profiles/followers/
    - Returns paginated list of profiles following the current user
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileOutSerializer

    def get_queryset(self):
        """Returns queryset of profiles following the current user."""
        profile = self.request.user.profile
        return profile.followers.select_related("user")


class FollowingsAPIView(ListAPIView):
    """API endpoint for listing who a user is following.
    
    GET /profiles/followings/
    - Returns paginated list of profiles the current user follows
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileOutSerializer

    def get_queryset(self):
        """Returns queryset of profiles the current user follows."""
        profile = self.request.user.profile
        return profile.following.select_related("user")