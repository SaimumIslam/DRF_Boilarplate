from base.repositories.base import BaseRepository

from ..models import Group


class GroupRepository(BaseRepository):
    def __init__(self):
        super().__init__(Group)
        self.MODULE_GROUPS = ["tuition", "coaching", "schooling"]

    def add_permission_by_permission__group_id(self, permission, group_id):
        instance = self.get_by_attr(pk=group_id)
        if instance:
            instance.permissions.add(permission)

    def remove_permission_by_permission__group_id(self, permission, group_id):
        instance = self.get_by_attr(pk=group_id)
        if instance:
            instance.permissions.remove(permission)

    def _get_all_names(self):
        return self.queryset.values_list("name", flat=True)

    def post_migration_create(self):
        existing_group_names = self._get_all_names()
        un_saved_groups = list(set(self.MODULE_GROUPS).difference(set(existing_group_names)))

        valid_items = [{"name": group_name} for group_name in un_saved_groups]
        self.bulk_create(valid_items)
