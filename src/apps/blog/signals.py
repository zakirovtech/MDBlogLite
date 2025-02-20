import logging
import os

from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.blog.models import Bio, Post
from apps.blog.tasks import delete_image

logger = logging.getLogger("blog")


@receiver(post_delete, sender=Bio)
def delete_image_on_bio_delete(sender, instance, **kwargs):
    if instance.image:
        path = instance.image.path
        name = str(instance)
        id = instance.id
        delete_image.delay(name, path, id)


@receiver(post_delete, sender=Post)
def delete_image_on_post_delete(sender, instance, **kwargs):
    if instance.image:
        path = instance.image.path
        name = str(instance)
        id = instance.id
        delete_image.delay(name, path, id)


@receiver(post_save, sender=Post)
def clear_post_cache_on_save(sender, instance, created, **kwargs):
    cache.delete("post_list_cache")
    logger.info(
        "Cache for Post_List objects is deleted after updating / (creating) a (new) post."
    )

    if not created:
        cache.delete(f"post_{instance.id}_detail_cache")
        logger.info(
            f"Cache for Post_Detail object {instance.id} is deleted after updating."
        )


@receiver(post_delete, sender=Post)
def clear_post_cache_on_delete(sender, instance, **kwargs):
    cache.delete("post_list_cache")
    logger.info(
        "Cache for Post_List objects is deleted after deleting a post."
    )

    cache.delete(f"post_{instance.id}_detail_cache")
    logger.info(
        f"Cache for Post_Detail object {instance.id} is deleted after deleting."
    )


@receiver(post_save, sender=Bio)
def clear_bio_cache_on_save(sender, instance, created, **kwargs):
    cache_key = "bio_show_cache"

    if not created:
        cache.delete(cache_key)
        logger.info(f"Cache for Bio object is deleted after updating.")


@receiver(post_delete, sender=Bio)
def clear_bio_cache_on_delete(sender, instance, **kwargs):
    cache_key = "bio_show_cache"
    cache.delete(cache_key)
    logger.info(f"Cache for Bio object is deleted after deletion.")
