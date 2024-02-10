
class BaseService:
    """
    We need a valid Repository class to init the Base Service.
        ```
        def __init__(self):
            super().__init__(ValidRepositoryClass)
        ```
    """

    def __init__(self, repository_class):
        self.repository = repository_class()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, pk):
        return self.repository.get_by_id(pk)

    def get_all_by_ids(self, pk):
        return self.repository.get_all_by_ids(pk)

    def get_id_by_attr(self, **filters):
        return self.repository.get_id_by_attr(**filters)

    def get_by_attr(self, **filters):
        return self.repository.get_by_attr(**filters)

    def filter(self, **filters):
        return self.repository.filter(**filters)

    def order_by(self, *order_by):
        return self.repository.order_by(*order_by)

    def create(self, **validated_data):
        return self.repository.create(**validated_data)

    def update(self, pk, **validated_data):
        return self.repository.update(pk, **validated_data)

    def bulk_create(self, valid_items):
        return self.repository.bulk_create(valid_items)
