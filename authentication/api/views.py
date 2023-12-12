from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from base.core import exceptions

from ..api.serializers import UserSerializer, ContentTypeSerializer, GroupSerializer, PermissionSerializer
from ..api.serializers import LoginSerializer, UserGroupSerializer, UserPermissionSerializer, GroupPermissionSerializer
from ..services.permission import PermissionService
from ..services.group import GroupService
from ..services.user import UserService
from ..models import Token, ContentType


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def login(request):
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(email=serializer.data["email"], password=serializer.data["password"])
    if not user:
        return Response({'detail': 'Invalid Credentials'}, status=status.HTTP_404_NOT_FOUND)

    token, _ = Token.objects.get_or_create(user=user, device_info=user_agent)

    response_data = UserSerializer(user).data
    response_data["token"] = token.key

    return Response(data=response_data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    token = Token.objects.filter(user=request.user, device_info=user_agent).first()
    if token:
        token.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_content_types(request):
    query_params = request.query_params

    filters = {}
    if query_params.get("app_label"):
        filters["app_label"] = query_params["app_label"]

    if query_params.get("model"):
        filters["model"] = query_params["model"]

    content_types = ContentType.objects.filter(**filters).all()
    serializer_data = ContentTypeSerializer(content_types, many=True).data
    return Response(status=status.HTTP_200_OK, data=serializer_data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_groups(request):
    group_service = GroupService()
    query_params = request.query_params

    filters = {}
    if query_params.get("name"):
        filters["name"] = query_params["name"]

    groups = group_service.filter(**filters)

    detail_fields = query_params.get("detail_fields", "")
    detail_fields = [field.strip() for field in detail_fields.split(",")]

    serializer_context = {
        "requested_user": getattr(request, 'user'),
        "detail_fields": detail_fields
    }

    serializer_data = GroupSerializer(groups, many=True, context=serializer_context).data
    return Response(status=status.HTTP_200_OK, data=serializer_data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_permissions(request):
    permission_service = PermissionService()
    query_params = request.query_params

    filters = {}
    if query_params.get("codename"):
        filters["codename"] = query_params["codename"]

    permissions = permission_service.filter(**filters)

    detail_fields = query_params.get("detail_fields", "")
    detail_fields = [field.strip() for field in detail_fields.split(",")]

    serializer_context = {
        "requested_user": getattr(request, 'user'),
        "detail_fields": detail_fields
    }

    serializer_data = PermissionSerializer(permissions, many=True, context=serializer_context).data
    return Response(status=status.HTTP_200_OK, data=serializer_data)


class UserPermissionAPIView(APIView):
    user_service = UserService()
    permission_service = PermissionService()

    def initial(self, request, *args, **kwargs):
        if request.method == "POST" or request.method == "DELETE":
            serializer = UserPermissionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

        return super().initial(request, *args, **kwargs)

    def get(self, request, **kwargs):
        user = request.query_params.get("user", "")
        if not user:
            raise exceptions.Unprocessable("Please provide user as query params")

        permissions = self.permission_service.filter(user=user)

        serializer_data = PermissionSerializer(permissions, many=True).data
        return Response(status=status.HTTP_200_OK, data=serializer_data)

    def post(self, request, **kwargs):
        user_id = request.data.get("user")
        permission_id = request.data.get("permission")

        permission = self.permission_service.get_by_id(permission_id)
        if permission:
            self.user_service.add_permission_by_permission__user_id(permission, user_id)

        # uncertainty and not returning anything that's why did not use 201
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, **kwargs):
        user_id = request.data.get("user")
        permission_id = request.data.get("permission")

        permission = self.permission_service.get_by_id(permission_id)
        if permission:
            self.user_service.remove_permission_by_permission__user_id(permission, user_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserGroupAPIView(APIView):
    user_service = UserService()
    group_service = GroupService()

    def initial(self, request, *args, **kwargs):
        if request.method == "POST" or request.method == "DELETE":
            serializer = UserGroupSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

        return super().initial(request, *args, **kwargs)

    def get(self, request, **kwargs):
        user = request.query_params.get("user", "")
        if not user:
            raise exceptions.Unprocessable("Please provide user as query params")

        groups = self.group_service.filter(user=user)

        serializer_data = GroupSerializer(groups, many=True).data
        return Response(status=status.HTTP_200_OK, data=serializer_data)

    def post(self, request, **kwargs):
        user_id = request.data.get("user")
        group_id = request.data.get("group")

        group = self.group_service.get_by_id(group_id)
        if group:
            self.user_service.add_group_by_group__user_id(group, user_id)

        # uncertainty and not returning anything that's why did not use 201
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, **kwargs):
        user_id = request.data.get("user")
        group_id = request.data.get("group")

        group = self.group_service.get_by_id(group_id)
        if group:
            self.user_service.remove_group_by_group__user_id(group, user_id)

        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupPermissionAPIView(APIView):
    permission_service = PermissionService()
    group_service = GroupService()

    def initial(self, request, *args, **kwargs):
        if request.method == "POST" or request.method == "DELETE":
            serializer = GroupPermissionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

        return super().initial(request, *args, **kwargs)

    def get(self, request, **kwargs):
        group = request.query_params.get("group", "")
        if not group:
            raise exceptions.Unprocessable("Please provide group as query params")

        permissions = self.permission_service.get_group_permissions_by_group(group)

        serializer_data = PermissionSerializer(permissions, many=True).data
        return Response(status=status.HTTP_200_OK, data=serializer_data)

    def post(self, request, **kwargs):
        group_id = request.data.get("group")
        permission_id = request.data.get("permission")

        permission = self.permission_service.get_by_id(permission_id)
        if permission:
            self.group_service.add_permission_by_permission__group_id(permission, group_id)

        # uncertainty and not returning anything that's why did not use 201
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, **kwargs):
        group_id = request.data.get("group")
        permission_id = request.data.get("permission")

        permission = self.permission_service.get_by_id(permission_id)
        if permission:
            self.group_service.remove_permission_by_permission__group_id(permission, group_id)

        return Response(status=status.HTTP_204_NO_CONTENT)
