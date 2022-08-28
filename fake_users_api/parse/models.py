from django.db import models
from . import utils
from . utils import Vk_api

class VkGroup(models.Model):
    group_id = models.CharField(max_length=255, unique=True)
    group_name = models.CharField(max_length=255)

    def save(self, *args, **kwargs) -> None:
        group_info = Vk_api.get_group_info(group_id=self.group_id) 
        self.group_name = group_info['name']
        return super().save(*args, **kwargs)

    class Meta:
        db_table = 'vk_group'


class VkUserRawData(models.Model):
    group = models.ForeignKey(VkGroup, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    photo_url = models.URLField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    saved = models.BooleanField(default=False)
    checked = models.BooleanField(default=False)


    class Meta:
        db_table = "vk_user_rawdata"