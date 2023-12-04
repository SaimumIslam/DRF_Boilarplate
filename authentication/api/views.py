from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from ..api.serializers import LoginSerializer, UserSerializer
from ..models import Token


@api_view(["POST", ])
@authentication_classes([])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = authenticate(email=serializer.data["email"], password=serializer.data["password"])
    if not user:
        return Response({'detail': 'Invalid Credentials'}, status=status.HTTP_404_NOT_FOUND)
    response = UserSerializer(user).data

    user_agent = request.META.get('HTTP_USER_AGENT', '')

    token, _ = Token.objects.get_or_create(user=user, device_info=user_agent)
    response["token"] = token.key

    return Response(data=response, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    token = Token.objects.filter(user=request.user, device_info=user_agent).first()
    if token:
        token.delete()
    return Response(status=status.HTTP_200_OK)
