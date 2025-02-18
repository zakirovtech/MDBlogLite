import re

import bleach
import markdown
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.html import mark_safe, strip_tags


class DateModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tag(DateModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("post-list-by-tag", kwargs={"tag": self.name})

    def save(self, *args, **kwargs) -> None:
        self.name = self.name.capitalize()
        return super().save(*args, **kwargs)


class Post(DateModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    header = models.CharField(max_length=128)
    body = models.TextField()
    image = models.ImageField(upload_to="posts", null=True, blank=True)
    ips = models.ManyToManyField("Ip", related_name="posts", blank=True)
    tags = models.ManyToManyField(to=Tag, related_name="posts")
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.header

    def get_body_as_html(self):
        html_body = markdown.markdown(self.body)

        html_body = re.sub(
            r"(<code.*?>)([\s\S]*?)(</code>)", r"<pre>\1\2\3</pre>", html_body
        )

        cleaned_body = bleach.clean(
            html_body,
            tags=settings.ALLOWED_TAGS,
            attributes=settings.ALLOWED_ATTRIBUTES,
        )
        return cleaned_body

    def get_truncated_body(self):
        truncated_markdown = markdown.markdown(self.body)[:100] + "..."
        return mark_safe(
            bleach.clean(
                truncated_markdown,
                tags=settings.ALLOWED_TAGS,
                attributes=settings.ALLOWED_ATTRIBUTES,
            )
        )

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"id": str(self.id)})

    def get_update_url(self):
        return reverse("post-update", kwargs={"id": str(self.id)})

    def get_delete_url(self):
        return reverse("post-delete", kwargs={"id": str(self.id)})


class Ip(DateModel):
    ip = models.GenericIPAddressField(null=True)
    is_restricted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.ip


class Bio(DateModel):
    body = models.TextField()
    image = models.ImageField(
        upload_to="avatars",
        default="default/default_avatar.png",
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Bio"
        verbose_name_plural = "Bios"

    def get_body_as_html(self):
        html_body = markdown.markdown(self.body)

        html_body = re.sub(
            r"(<code.*?>)([\s\S]*?)(</code>)", r"<pre>\1\2\3</pre>", html_body
        )

        cleaned_body = bleach.clean(
            html_body,
            tags=settings.ALLOWED_TAGS,
            attributes=settings.ALLOWED_ATTRIBUTES,
        )
        return cleaned_body

    def save(self, *args, **kwargs):
        if not self.pk and Bio.objects.exists():
            raise ValueError("Only one Bio instance is allowed.")

        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return "Bio"
