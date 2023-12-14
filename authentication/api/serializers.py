from rest_framework import serializers
from django.contrib.auth.models import ContentType

from base.api.serializers import BaseModelSerializer

from .minimal_serializers import InstituteMinimalSerializer, BranchMinimalSerializer
from ..models import User, Institute, Branch, Profile, Group, Permission

from ..services.user import UserService


class InstituteSerializer(BaseModelSerializer):
    class Meta:
        model = Institute
        fields = ["id", "name", "address", "email", "mobile"]


class BranchSerializer(BaseModelSerializer):
    class Meta:
        model = Branch
        fields = ["id", "name", "email", "mobile", "address", "timezone", "institute"]

    def to_representation(self, instance):
        response_data = super().to_representation(instance)
        detail_fields = self.context.get("detail_fields", [])

        if "institute" in detail_fields:
            response_data["institute"] = InstituteMinimalSerializer(instance.institute).data

        return response_data


class UserSerializer(BaseModelSerializer):
    user_service = UserService()
    branch = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "role", "last_login", "branch"]

    def to_representation(self, instance):
        response_data = super().to_representation(instance)
        response_data["full_name"] = instance.get_full_name()

        detail_fields = self.context.get("detail_fields", [])

        if "branch" in detail_fields:
            response_data["branch"] = BranchMinimalSerializer(instance.branch).data

        if "profile" in detail_fields and hasattr(instance, "profile"):
            response_data["profile"] = ProfileSerializer(instance.profile).data

        return response_data


class ProfileSerializer(BaseModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "mobile", "address", "student_id", "photo", "timezone", "last_activity_at", "user"]

    def to_representation(self, instance):
        response_data = super().to_representation(instance)

        user_data = UserSerializer(instance.user, context=self.context).data
        response_data.update(user_data)  # merge profile dict and user dict and override common key
        response_data["id"] = instance.id  # reset overrode id with instance

        return response_data


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]

    def to_representation(self, instance):
        response_data = super().to_representation(instance)
        detail_fields = self.context.get("detail_fields", [])

        if "permissions" in detail_fields:
            response_data["permissions"] = PermissionSerializer(instance.permissions, many=True).data

        return response_data


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        exclude = ["name"]

    def to_representation(self, instance):
        response_data = super().to_representation(instance)
        detail_fields = self.context.get("detail_fields", [])

        if "content_type" in detail_fields:
            response_data["content_type"] = ContentTypeSerializer(instance.content_type).data

        return response_data


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = "__all__"


# only validation_serializer

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserPermissionSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    permission = serializers.IntegerField()


class UserGroupSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    group = serializers.IntegerField()


class GroupPermissionSerializer(serializers.Serializer):
    group = serializers.IntegerField()
    permission = serializers.IntegerField()
