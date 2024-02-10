class BaseRepository:
    def __init__(self, model_class):
        self.model = model_class
        self.queryset = model_class.objects.filter()

    def get_all(self):
        return self.queryset

    def get_all_ids(self):
        return list(self.queryset.values_list("id", flat=True))

    def get_all_by_ids(self, ids):
        return self.queryset.filter(id__in=ids)

    def get_by_id(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return None

    def get_by_attr(self, **filters):
        return self.queryset.filter(**filters).first()

    def get_id_by_attr(self, **filters):
        instance = self.queryset.filter(**filters).first()
        return getattr(instance, 'id', None)

    def filter(self, **filters):
        return self.queryset.filter(**filters)

    def update(self, pk, **validated_data):
        target_object = self.queryset.filter(id=pk).first()

        if not target_object:
            print(f"PK not found in update! pk: {pk}")
            return

        for key, value in validated_data.items():
            setattr(target_object, key, value)

        target_object.save()
        target_object.refresh_from_db()
        return target_object

    def order_by(self, *order_by):
        return self.queryset.order_by(order_by)

    def create(self, **validated_data):
        return self.model.objects.create(**validated_data)

    def bulk_create(self, valid_items):
        instances = []
        for item in valid_items:
            instance = self.model(**item)
            instances.append(instance)
        self.model.objects.bulk_create(instances)
