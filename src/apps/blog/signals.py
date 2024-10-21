from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings

import os

from apps.blog.models import Bio

@receiver(post_delete, sender=Bio)
def delete_image_on_bio_delete(sender, instance, **kwargs):
    if instance.image:
        image_path = instance.image.path

        if os.path.exists(image_path) and "default" not in image_path:
            os.remove(image_path)
