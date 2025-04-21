from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _
from rest_framework import status

class CantRateOwnArticle(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('You cannot rate your own article.')
    default_code = 'forbidden'
    
    
    
class CantClapOwnArticle(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('You cannot clap for your own article.')
    default_code = 'forbidden'
    
class CantCommentOwnArticle(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('You cannot comment on your own article.')
    default_code = 'forbidden'