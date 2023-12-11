from rest_framework.authentication import TokenAuthentication

from ..models import Token


class UserTokenAuthentication(TokenAuthentication):
    model = Token

