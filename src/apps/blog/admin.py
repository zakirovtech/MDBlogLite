from django.conf import settings
from django.contrib import admin

from apps.blog.models import Bio, Ip, Post, Tag


class TagInline(admin.TabularInline):
    model = Post.tags.through


class PostInline(admin.TabularInline):
    model = Post.tags.through


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "date_created",
        "date_updated",
        "author",
        "header",
        "body",
    )
    search_fields = ("header", "date_created")
    inlines = [TagInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "date_created", "date_updated", "name")
    search_fields = ("name", "date_created")
    inlines = [PostInline]


@admin.register(Ip)
class IpAdmin(admin.ModelAdmin):
    list_display = ("pk", "ip", "date_created", "date_updated")
    search_fields = ("ip", "date_created")


@admin.register(Bio)
class BioAdmin(admin.ModelAdmin):
    list_display = ("id", "date_created", "date_updated", "body")
    search_fields = ("date_created",)


class MyAdminSite(admin.AdminSite):
    site_header = settings.BLOG_NAME
    site_title = "Мой сайт"
    index_title = "Добро пожаловать в админку"


admin_site = MyAdminSite(name="admin")
