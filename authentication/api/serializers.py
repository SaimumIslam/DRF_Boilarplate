from rest_framework import serializers

from base.api.serializers import BaseModelSerializer

from .minimal_serializers import InstituteMinimalSerializer, BranchMinimalSerializer
from ..models import User, Institute, Branch, Profile

from ..services.user import UserService


class InstituteSerializer(BaseModelSerializer):
    class Meta:
        model = Institute
        fields = ["id", "name", "address", "email", "mobile"]


class BranchSerializer(BaseModelSerializer):
    class Meta:
        model = Branch
        fields = ["id", "name", "email", "mobile", "address", "timezone"]

    def to_representation(self, instance):
        response_data = super().to_representation(instance)
        detail_fields = self.context.get("detail_fields", [])

        if "institute" in detail_fields:
            response_data["institute"] = InstituteMinimalSerializer(instance.institute).data

        return response_data


class UserSerializer(BaseModelSerializer):
    user_service = UserService()

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "role", "last_login"]

    def validate_branch(self, value):
        user = self.context["user"]
        if not user.is_superuser and user.branch != value:
            return serializers.ValidationError("Please provide branch")

        return value

    def to_representation(self, instance):
        response_data = super().to_representation(instance)
        response_data["full_name"] = instance.get_full_name()
        response_data["role_display"] = instance.get_role_display()

        detail_fields = self.context.get("detail_fields", [])

        if "branch" in detail_fields:
            response_data["branch"] = BranchMinimalSerializer(instance.branch).data

        if "profile" in detail_fields and hasattr(instance, "profile"):
            response_data["profile"] = ProfileSerializer(instance.profile).data

        return response_data


class ProfileSerializer(BaseModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "mobile", "address", "student_id", "photo", "timezone", "last_activity_at"]

    def to_representation(self, instance):
        response_data = super().to_representation(instance)

        user_data = UserSerializer(instance.user, context=self.context).data
        response_data.update(user_data)  # merge profile dict and user dict and override common key
        response_data["id"] = instance.id  # reset overrode id with instance

        return response_data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
