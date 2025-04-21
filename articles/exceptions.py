from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _
from rest_framework import status

class CantRateOwnArticle(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('A server error occurred.')
    default_code = 'forbidden'
    
    
    
class CantClapOwnArticle(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('A server error occurred.')
    default_code = 'forbidden'
    
class CantCommentOwnArticle(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('A server error occurred.')
    default_code = 'forbidden'