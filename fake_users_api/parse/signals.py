from django.db.models.signals import post_save
from django.dispatch import receiver
from . import models
from . import tasks


@receiver(post_save, sender=models.VkGroup)
def save_image_to_model(sender,instance, **kwargs):
    tasks.parse_user_info.delay(instance.group_id)