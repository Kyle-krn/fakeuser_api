from django.db import models
from .utils import Vk_api

class VkGroup(models.Model):
    group_id = models.CharField(max_length=255, unique=True)
    group_name = models.CharField(max_length=255)

    def save(self, *args, **kwargs) -> None:
        group_info = Vk_api.get_group_info(group_id=self.group_id) 
        self.group_name = group_info['name']
        return super().save(*args, **kwargs)

    class Meta:
        db_table = 'vk_group'
