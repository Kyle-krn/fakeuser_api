from django.db import models


class VkGroupCounter(models.Model):
    group_id = models.CharField(max_length=255)
    last_user_id = models.IntegerField(null=True)
    last_page = models.IntegerField(null=True)
    count_save_photo = models.IntegerField(default=0)

    class Meta:
        db_table = 'vk_group_counter'
