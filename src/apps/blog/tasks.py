import logging
import os

from celery import shared_task
from django.conf import settings
from sentry_sdk import capture_exception

logger = logging.getLogger("blog")


@shared_task
def delete_image(
    instance_name: str, image_path: str, instance_id: int
) -> None:
    try:
        if os.path.exists(image_path) and "default" not in image_path:
            os.remove(image_path)
            logger.info(
                f"Image was deleted from file system after deleting an object: [{instance_name}] with id: [{instance_id}]"
            )
    except Exception as e:
        logger.error(
            f"Error while deleting image for {instance_name} with id {instance_id}: {e}"
        )
        if settings.SENTRY_STATUS:
            capture_exception(e)
