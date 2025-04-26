from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _
from rest_framework import status


class CantRateOwnArticle(APIException):
    """
    Exception raised when a user attempts to rate their own article.
    
    This exception returns a 403 Forbidden status code and indicates that
    self-rating of articles is not permitted in the system.
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('You cannot rate your own article.')
    default_code = 'forbidden'


class CantClapOwnArticle(APIException):
    """
    Exception raised when a user attempts to clap for their own article.
    
    This exception returns a 403 Forbidden status code and indicates that
    self-appreciation via claps is not permitted in the system.
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('You cannot clap for your own article.')
    default_code = 'forbidden'


class CantCommentOwnArticle(APIException):
    """
    Exception raised when a user attempts to comment on their own article.
    
    This exception returns a 403 Forbidden status code and indicates that
    self-commenting on articles is not permitted in the system.
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('You cannot comment on your own article.')
    default_code = 'forbidden'