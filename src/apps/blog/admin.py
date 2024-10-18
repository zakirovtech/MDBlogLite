from django.contrib import admin
from apps.blog.models import Bio, Post, Ip


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "date_created", "date_updated", "author", "header", "body")
    search_fields = ("header", "date_created")


@admin.register(Ip)
class IpAdmin(admin.ModelAdmin):
    list_display = ("pk", "ip", "date_created", "date_updated")
    search_fields = ("ip", "date_created")


@admin.register(Bio)
class BioAdmin(admin.ModelAdmin):
    list_display = ("id", "date_created", "date_updated", "body")
    search_fields = ("date_created",)

