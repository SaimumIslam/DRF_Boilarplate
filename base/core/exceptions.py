from rest_framework.exceptions import APIException, status
from django.utils.translation import gettext_lazy as _


class NOTImplemented(APIException):
    status_code = status.HTTP_501_NOT_IMPLEMENTED
    default_detail = _('Not implemented.')
    default_code = 'not_implemented'


class AttributeNotFound(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('Attribute not found.')
    default_code = 'attribute_not_found'


class Conflicted(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _('Conflicts with existing entry.')
    default_code = 'conflict'


class DBError(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = _('Database service error')
    default_code = 'db_service'
