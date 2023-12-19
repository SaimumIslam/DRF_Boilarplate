def default_permission(func):
    def decorator(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return func(self, request, *args, **kwargs)

    return decorator

