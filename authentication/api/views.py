from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from drf_spectacular.utils import extend_schema

from base.core.exceptions import Unprocessable
from base.core.pagination import ViewLimitOffsetPagination

from authentication.core.permissions import HasApiPermissions

from ..api.serializers import UserSerializer, ContentTypeSerializer, GroupSerializer, PermissionSerializer
from ..api.serializers import LoginSerializer, UserGroupSerializer, UserPermissionSerializer, GroupPermissionSerializer
from ..api.serializers import GroupRestrictionSerializer, UserRestrictionSerializer
from ..services.permission import PermissionService
from ..services.group import GroupService
from ..services.user import UserService
from ..models import Token, ContentType

from ..utils.helper_func import get_client_ip, get_client_agent


@extend_schema(request=LoginSerializer, responses=UserSerializer)
@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(email=serializer.data["email"], password=serializer.data["password"])
    if not user:
        return Response({'detail': 'Invalid Credentials'}, status=status.HTTP_404_NOT_FOUND)

    user_agent = get_client_agent(request)
    user_ip = get_client_ip(request)

    token, _ = Token.objects.get_or_create(user=user, device_info=user_agent, device_ip=user_ip)

    response_data = UserSerializer(user).data
    response_data["token"] = token.key

    return Response(data=response_data, status=status.HTTP_200_OK)


@extend_schema(request=None, responses=None)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    token = Token.objects.filter(user=request.user, device_info=user_agent).first()
    if token:
        token.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(responses=ContentTypeSerializer)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_content_types(request):
    query_params = request.query_params

    filters = {}
    if query_params.get("app_label"):
        filters["app_label"] = query_params["app_label"]

    if query_params.get("model"):
        filters["model"] = query_params["model"]

    queryset = ContentType.objects.filter(**filters)

    return ViewLimitOffsetPagination.get_paginated_response(request=request,
                                                            queryset=queryset,
                                                            serializer=ContentTypeSerializer)


@extend_schema(responses=PermissionSerializer)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_permissions(request):
    permission_service = PermissionService()
    query_params = request.query_params

    detail_fields = query_params.get("detail_fields", "")
    detail_fields = [field.strip() for field in detail_fields.split(",")]

    serializer_context = {
        "requested_user": getattr(request, 'user'),
        "detail_fields": detail_fields
    }

    filters = {}
    if query_params.get("codename"):
        filters["codename"] = query_params["codename"]

    if query_params.get("content_type"):
        filters["content_type"] = query_params["content_type"]

    queryset = permission_service.filter(**filters).order_by('id')

    return ViewLimitOffsetPagination.get_paginated_response(request=request,
                                                            queryset=queryset,
                                                            context=serializer_context,
                                                            serializer=PermissionSerializer)


class UserPermissionAPIView(APIView):
    user_service = UserService()
    permission_service = PermissionService()

    def initial(self, request, *args, **kwargs):
        if request.method == "POST" or request.method == "DELETE":
            serializer = UserPermissionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

        return super().initial(request, *args, **kwargs)

    @extend_schema(responses=PermissionSerializer)
    def get(self, request, **kwargs):
        user = request.query_params.get("user", "")
        if not user:
            raise Unprocessable("Please provide user as query params")

        permissions = self.permission_service.filter(user=user)
        return ViewLimitOffsetPagination.get_paginated_response(request=request,
                                                                queryset=permissions,
                                                                serializer=PermissionSerializer)

    @extend_schema(request=UserPermissionSerializer, responses=None)
    def post(self, request, **kwargs):
        user_id = request.data.get("user")
        permission_id = request.data.get("permission")

        permission = self.permission_service.get_by_id(permission_id)
        if permission:
            self.user_service.add_permission_by_permission__user_id(permission, user_id)

        # uncertainty and not returning anything that's why did not use 201
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(request=UserPermissionSerializer, responses=None)
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

    @extend_schema(responses=GroupSerializer)
    def get(self, request, **kwargs):
        user = request.query_params.get("user", "")
        if not user:
            raise Unprocessable("Please provide user as query params")

        groups = self.group_service.filter(user=user)
        return ViewLimitOffsetPagination.get_paginated_response(request=request,
                                                                queryset=groups,
                                                                serializer=GroupSerializer)

    @extend_schema(request=UserGroupSerializer, responses=None)
    def post(self, request, **kwargs):
        user_id = request.data.get("user")
        group_id = request.data.get("group")

        group = self.group_service.get_by_id(group_id)
        if group:
            self.user_service.add_group_by_group__user_id(group, user_id)

        # uncertainty and not returning anything that's why did not use 201
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(request=UserGroupSerializer, responses=None)
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

    @extend_schema(request=PermissionSerializer, responses=None)
    def get(self, request, **kwargs):
        group_id = request.query_params.get("group", "")

        group = self.group_service.get_by_id(group_id)
        if not group:
            raise Unprocessable("Please provide valid group as query params")

        permissions = group.permissions.all()
        return ViewLimitOffsetPagination.get_paginated_response(request=request,
                                                                queryset=permissions,
                                                                serializer=PermissionSerializer)

    @extend_schema(request=GroupPermissionSerializer, responses=None)
    def post(self, request, **kwargs):
        group_id = request.data.get("group")
        permission_id = request.data.get("permission")

        permission = self.permission_service.get_by_id(permission_id)
        if permission:
            self.group_service.add_permission_by_permission__group_id(permission, group_id)

        # uncertainty and not returning anything that's why did not use 201
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(request=GroupPermissionSerializer, responses=None)
    def delete(self, request, **kwargs):
        group_id = request.data.get("group")
        permission_id = request.data.get("permission")

        permission = self.permission_service.get_by_id(permission_id)
        if permission:
            self.group_service.remove_permission_by_permission__group_id(permission, group_id)

        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupRestrictionAPIView(APIView):
    permission_service = PermissionService()
    group_service = GroupService()

    def initial(self, request, *args, **kwargs):
        if request.method == "POST" or request.method == "DELETE":
            serializer = GroupRestrictionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

        return super().initial(request, *args, **kwargs)

    @extend_schema(request=PermissionSerializer, responses=None)
    def get(self, request, **kwargs):
        group_id = request.query_params.get("group", "")

        group = self.group_service.get_by_id(group_id)
        if not group:
            raise Unprocessable("Please provide valid group as query params")

        restriction_ids = group.group_restrictions.values_list("restriction", flat=True)
        restrictions = self.permission_service.get_all_by_ids(restriction_ids)
        return ViewLimitOffsetPagination.get_paginated_response(request=request,
                                                                queryset=restrictions,
                                                                serializer=PermissionSerializer)

    @extend_schema(request=GroupRestrictionSerializer, responses=None)
    def post(self, request, **kwargs):
        group_id = request.data.get("group")
        restriction_id = request.data.get("restriction")

        restriction = self.permission_service.get_by_id(restriction_id)
        if restriction:
            self.group_service.add_restriction_by_restriction__group_id(restriction, group_id)

        # uncertainty and not returning anything that's why did not use 201
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(request=GroupRestrictionSerializer, responses=None)
    def delete(self, request, **kwargs):
        group_id = request.data.get("group")
        restriction_id = request.data.get("restriction")

        restriction = self.permission_service.get_by_id(restriction_id)
        if restriction:
            self.group_service.remove_restriction_by_restriction__group_id(restriction, group_id)

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserRestrictionAPIView(APIView):
    user_service = UserService()
    permission_service = PermissionService()

    def initial(self, request, *args, **kwargs):
        if request.method == "POST" or request.method == "DELETE":
            serializer = UserRestrictionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

        return super().initial(request, *args, **kwargs)

    @extend_schema(responses=PermissionSerializer)
    def get(self, request, **kwargs):
        user = request.query_params.get("user", "")
        if not user:
            raise Unprocessable("Please provide user as query params")

        restrictions = self.permission_service.filter(r_user=user)
        return ViewLimitOffsetPagination.get_paginated_response(request=request,
                                                                queryset=restrictions,
                                                                serializer=PermissionSerializer)

    @extend_schema(request=UserRestrictionSerializer, responses=None)
    def post(self, request, **kwargs):
        user_id = request.data.get("user")
        restriction_id = request.data.get("restriction")

        restriction = self.permission_service.get_by_id(restriction_id)
        if restriction:
            self.user_service.add_restriction_by_restriction__user_id(restriction, user_id)

        # uncertainty and not returning anything that's why did not use 201
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(request=UserRestrictionSerializer, responses=None)
    def delete(self, request, **kwargs):
        user_id = request.data.get("user")
        restriction_id = request.data.get("restriction")

        restriction = self.permission_service.get_by_id(restriction_id)
        if restriction:
            self.user_service.remove_restriction_by_restriction__user_id(restriction, user_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
