# exceptions.py
from rest_framework.exceptions import APIException
from rest_framework import status
from django.utils.translation import gettext_lazy as _


class CantFollowYourself(APIException):
    """
    Custom API exception for when a user attempts to follow themselves.

    This exception is raised with a 403 Forbidden status code when a user
    tries to perform a follow action on their own profile.
    """

    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _("You can't follow your own account.")
    default_code = 'forbidden'