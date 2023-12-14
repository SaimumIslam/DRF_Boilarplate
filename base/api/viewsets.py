from rest_framework import viewsets

from ..mixins.utility import UtilityMixin


class ModelViewset(UtilityMixin, viewsets.ModelViewSet):
    minimal_serializer_class = None

    def get_queryset(self):
        model = super().get_queryset().model
        model_fields = [field.name for field in model._meta.get_fields()]

        order_by = self.request.query_params.get("order_by")
        if order_by in model_fields:
            return super().get_queryset().order_by(order_by)
        return super().get_queryset()

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        return serializer.save(updated_by=self.request.user)

    def get_serializer_class(self):
        query_params = self.request.query_params

        if query_params.get("minimal") == '1':
            if self.minimal_serializer_class is None:
                raise AttributeError("Minimal serializer is not implemented yet.")
            return self.minimal_serializer_class or super().get_serializer_class()

        return super().get_serializer_class()

    def get_serializer_context(self):
        raw_detail_fields = self.request.query_params.get("detail_fields", "").split(",")
        detail_fields = self.clean_array_params(raw_detail_fields)

        raw_extra_fields = self.request.query_params.get("extra_fields", "").split(",")
        extra_fields = self.clean_array_params(raw_extra_fields)

        context = {
            **super().get_serializer_context(),
            "extra_fields": ','.join(extra_fields),
            "detail_fields": ','.join(detail_fields),
            "requested_user": getattr(self.request, 'user'),
        }
        return context
