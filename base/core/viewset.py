class UtilityMixin:
    def clean_array_params(self, items):
        return [item.strip() for item in items if item.strip()]