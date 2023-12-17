from django.utils import timezone
from django.core.cache import cache


class LastActivityMiddleware:
    """Records last activity of a user."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not request.user.is_authenticated:
            return response

        last_activity_timeout = 5 * 60  # 5 min expiration
        last_activity_cache_key = f'{request.user.id}_last_activity'

        if cache.get(last_activity_cache_key, version=1):
            return response

        cache.set(last_activity_cache_key, timezone.now(), timeout=last_activity_timeout, version=1)
        if hasattr(request.user, "profile"):
            request.user.profile.last_activity_at = timezone.now()
            request.user.profile.save()

        return response
