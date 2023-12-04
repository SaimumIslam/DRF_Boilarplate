from base.repositories.base import BaseRepository
from django.contrib.auth.models import Group


class GroupRepository(BaseRepository):
    def __init__(self):
        super().__init__(Group)
        self.MODULE_GROUPS = ["tuition", "coaching", "schooling"]

    def has_access_by_group_name__user(self, group_name, user):
        group = self.get_by_attr(name=group_name)
        if group:
            return group.user_set.filter(id=user.id).exists()
        return False

    def add_to_group_by_group_name__user(self, group_name, user):
        group = self.get_by_attr(name=group_name)
        if group:
            group.user_set.add(user)

    def get_all_names(self):
        return self.queryset.values_list("name", flat=True)

    def post_migration_create(self):
        existing_group_names = self.get_all_names()
        un_saved_groups = list(set(self.MODULE_GROUPS).difference(set(existing_group_names)))

        valid_items = [{"name": group_name} for group_name in un_saved_groups]
        self.bulk_create(valid_items)
