from rest_framework import serializers
from base.api.minimal_serializers import BaseModelMinimalSerializer

from ..models import User, Institute, Branch, Profile


class InstituteMinimalSerializer(BaseModelMinimalSerializer):
    class Meta:
        model = Institute
        fields = ["id", "name"]
        read_only_fields = fields


class BranchMinimalSerializer(BaseModelMinimalSerializer):
    class Meta:
        model = Branch
        fields = ["id", "name"]
        read_only_fields = fields

    def to_representation(self, instance):
        response_data = super().to_representation(instance)
        detail_fields = self.context.get("detail_fields", [])

        if "institute" in detail_fields:
            response_data["institute"] = InstituteMinimalSerializer(instance.institute).data

        return response_data


class UserMinimalSerializer(BaseModelMinimalSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]
        read_only_fields = fields

    def to_representation(self, instance):
        response_data = super().to_representation(instance)
        response_data["full_name"] = instance.get_full_name()

        detail_fields = self.context.get("detail_fields", [])

        if "branch" in detail_fields:
            response_data["branch"] = BranchMinimalSerializer(instance.branch).data

        if "profile" in detail_fields:
            response_data["profile"] = ProfileMinimalSerializer(instance.profile).data

        return response_data


class ProfileMinimalSerializer(BaseModelMinimalSerializer):
    class Meta:
        model = Profile
        fields = ["id", "mobile", "student_id", "photo"]

    def to_representation(self, instance):
        response_data = super().to_representation(instance)

        user_data = UserMinimalSerializer(instance.user, context=self.context).data
        response_data.update(user_data)  # merge profile dict and user dict and override common key
        response_data["id"] = instance.id  # reset overrode id with instance

        return response_data
