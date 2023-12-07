from rest_framework import viewsets


class BaseModelViewset(viewsets.ModelViewSet):
    minimal_serializer_class = None

    def get_queryset(self):
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
        detail_fields = [field.strip() for field in raw_detail_fields if field.strip()]

        raw_extra_fields = self.request.query_params.get("extra_fields", "").split(",")
        extra_fields = [field.strip() for field in raw_extra_fields if field.strip()]

        context = {
            **super().get_serializer_context(),
            "extra_fields": ','.join(extra_fields),
            "detail_fields": ','.join(detail_fields),
            "requested_user": getattr(self.request, 'user'),
        }
        return context
