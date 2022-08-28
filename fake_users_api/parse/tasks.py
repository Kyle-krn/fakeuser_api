from celery import shared_task
from . import models
from . import utils

@shared_task
def saved_raw_user_info(group_id: str):  
    offset = 0
    group = models.VkGroup.objects.get(group_id=group_id)

    group_members_info = utils.Vk_api.get_group_members(group_id=group_id, fields="photo_400_orig", offset=offset)
    while len(group_members_info) > 0:
        for member in group_members_info:
            if 'photo_400_orig' not in member:
                continue

            models.VkUserRawData.objects.get_or_create(user_id=member['id'], 
                                                       first_name=member['first_name'], 
                                                       last_name=member['last_name'],
                                                       photo_url=member['photo_400_orig'],
                                                       group=group)
        
        offset += len(group_members_info)
        group_members_info = utils.Vk_api.get_group_members(group_id=group_id, fields="photo_400_orig", offset=offset)



