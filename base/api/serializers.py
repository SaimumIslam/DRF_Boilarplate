from rest_framework import serializers
from authentication.api.minimal_serializers import UserMinimalSerializer


class BaseModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        raw_detail_fields = self.context.get("detail_fields", "").split(",")
        detail_fields = [field.strip() for field in raw_detail_fields if field.strip()]

        requested_user = self.context.get("requested_user", [])

        self.detail_fields = detail_fields
        self.requested_user = requested_user

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if "created_by" in self.detail_fields and hasattr(instance, "created_by"):
            data["created_by"] = UserMinimalSerializer(instance.created_by).data

        if "updated_by" in self.detail_fields and hasattr(instance, "updated_by"):
            data["updated_by"] = UserMinimalSerializer(instance.created_by).data

        return data
