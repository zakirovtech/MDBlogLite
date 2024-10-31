import debug_toolbar

from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    path(f"{settings.ADMIN_ENTRYPOINT}", admin.site.urls),
    path("", include("apps.blog.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = f"{settings.BLOG_NAME}"
admin.site.site_title = f"{settings.BLOG_NAME}"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path("__debug__", include(debug_toolbar.urls))]