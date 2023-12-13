def default_permission(func):
    def decorator(self, request, view, *args, **kwargs):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return func(self, request, view, *args, **kwargs)

    return decorator

