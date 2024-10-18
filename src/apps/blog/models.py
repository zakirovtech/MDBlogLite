from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    header = models.CharField(max_length=128)
    body = models.TextField()
    ips = models.ManyToManyField("Ip", related_name="posts", blank=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.header
    
    def get_post_views(self):
        return self.ips.count()
        
    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"id": str(self.id)})
    
    def get_update_url(self):
        return reverse("post-update", kwargs={"id": str(self.id)})
    
    def get_delete_url(self):
        return reverse("post-delete", kwargs={"id": str(self.id)})
    

class Ip(models.Model):
    ip = models.GenericIPAddressField(null=True)
    is_restricted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.ip


class Bio(models.Model):
    body = models.TextField()
    image = models.ImageField(upload_to="bio_avatars", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Bio"
        verbose_name_plural = "Bios"

    def save(self, *args, **kwargs):
        if not self.pk and Bio.objects.exists():
            raise ValueError("Only one Bio instance is allowed.")
        super().save(*args, **kwargs)
