from rest_framework.exceptions import APIException
from rest_framework import status
from django.utils.translation import gettext_lazy as _


class CantFollowYourself(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _("You can't follow your own account.")
    default_code = 'forbidden'