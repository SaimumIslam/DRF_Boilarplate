from rest_framework import serializers


class ModelMinimalSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        requested_user = self.context.get("requested_user", [])

        raw_detail_fields = self.context.get("detail_fields", "").split(",")
        detail_fields = [field.strip() for field in raw_detail_fields if field.strip()]

        raw_extra_fields = self.context.get("extra_fields", "").split(",")
        extra_fields = [field.strip() for field in raw_extra_fields if field.strip()]

        self.extra_fields = extra_fields
        self.detail_fields = detail_fields
        self.requested_user = requested_user

    def to_representation(self, instance):
        data = super().to_representation(instance)

        for field in self.extra_fields:
            if hasattr(instance, field):
                data[field] = getattr(instance, field)

        return data
