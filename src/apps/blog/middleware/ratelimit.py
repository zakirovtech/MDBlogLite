import logging

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseForbidden

logger = logging.getLogger("blog")


class RateLimitMiddleware:
    """Simple security anti-ddos middleware"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        request_count_key = f'rate_limit_{ip}'
        ban_key = f'banned_{ip}'

        if cache.get(ban_key):
            logger.warning(f"[Banned IP: {ip}] SEND REQUESTS")
            return HttpResponseForbidden("Too many requests - you are temporarily banned.")

        request_count = cache.get(request_count_key, 0)

        if request_count >= int(settings.RATE_LIMIT_VALUE):
            cache.set(ban_key, True, timeout=int(settings.BAN_TIMEOUT))
            logger.warning(f"[Banned IP: {ip}] SEND REQUESTS")
            return HttpResponseForbidden("Too many requests - you are temporarily banned.")

        cache.set(request_count_key, request_count + 1, timeout=int(settings.RATE_LIMIT_WINDOW))

        response = self.get_response(request)
        return response
    