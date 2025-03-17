import logging

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseForbidden

security_logger = logging.getLogger("login")


class RateLimitMiddleware:
    """Simple security anti-ddos middleware"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get(
            "HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR")
        )

        if ip and "," in ip:
            ip = ip.split(",")[0].strip()

        request_count_key = f"rate_limit_{ip}"
        ban_key = f"banned_{ip}"

        if request.user.is_staff:
            return self.get_response(request)

        if cache.get(ban_key):
            security_logger.warning(f"[Banned IP: {ip}] SEND REQUESTS")
            return HttpResponseForbidden(
                "Too many requests - you are temporarily banned."
            )

        request_count = cache.get(request_count_key, 0)

        if request_count >= int(settings.RATE_LIMIT_VALUE):
            cache.delete(request_count_key)
            cache.set(ban_key, True, timeout=int(settings.BAN_TIMEOUT))
            security_logger.warning(f"[Banned IP: {ip}] SEND REQUESTS")
            return HttpResponseForbidden(
                "Too many requests - you are temporarily banned."
            )

        cache.set(
            request_count_key,
            request_count + 1,
            timeout=int(settings.RATE_LIMIT_WINDOW),
        )

        response = self.get_response(request)
        return response
