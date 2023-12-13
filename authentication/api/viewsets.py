from django.db.models import Q, Value
from django.db.models.functions import Concat

from base.api.viewsets import BaseModelViewset
from authentication.core.permissions import HasApiPermissions, IsSuperAdmin, IsInstituteAdmin, IsAdmins

from .. import models
from . import serializers
from . import minimal_serializers


class InstituteViewset(BaseModelViewset):
    queryset = models.Institute.objects.filter()
    serializer_class = serializers.InstituteSerializer
    minimal_serializer_class = minimal_serializers.InstituteMinimalSerializer

    permission_classes = [IsSuperAdmin | IsInstituteAdmin]  # or operation


class BranchViewset(BaseModelViewset):
    queryset = models.Branch.objects.filter()
    serializer_class = serializers.BranchSerializer
    minimal_serializer_class = minimal_serializers.BranchMinimalSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAdmins]
        else:
            permission_classes = [IsAdmins, HasApiPermissions]  # and operation
        return [permission() for permission in permission_classes]


class UserViewset(BaseModelViewset):
    queryset = models.User.objects.filter()
    serializer_class = serializers.UserSerializer
    minimal_serializer_class = minimal_serializers.UserMinimalSerializer

    def get_queryset(self):
        query_params = self.request.query_params

        email = query_params.get("email")
        roles = query_params.get("roles", "")
        roles = self.clean_array_params(roles)

        or_filters = Q()
        filters = {
            "branch": self.request.user.branch
        }

        if email:
            filters["email"] = email
        if roles:
            filters["role__in"] = roles

        queryset = super().get_queryset().filter(or_filters, **filters)
        return queryset

    def perform_create(self, serializer):
        return serializer.save(branch=self.request.user.branch)


class ProfileViewset(BaseModelViewset):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    minimal_serializer_class = minimal_serializers.ProfileMinimalSerializer

    def get_queryset(self):
        query_params = self.request.query_params

        email = query_params.get("email")
        keyword = query_params.get("keyword")
        roles = query_params.get("roles", "")
        roles = self.clean_array_params(roles)

        or_filters = Q()
        filters = {
            "user__branch": self.request.user.branch
        }
        if keyword:
            or_filters = (Q(user__full_name__icontains=keyword) |
                          Q(user__email__icontains=keyword) |
                          Q(mobile__icontains=keyword) |
                          Q(student_id__icontains=keyword))
        if email:
            filters["user__email"] = email
        if roles:
            filters["user__role__in"] = roles

        queryset = super().get_queryset() \
            .annotate(full_name=Concat('user__first_name', Value(' '), 'user__last_name')) \
            .filter(or_filters, **filters)

        return queryset
