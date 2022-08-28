from vk_api import VkApi
from django.conf import settings
from . import models



def get_group_members_for_view(group_id: str):
    group = models.VkGroup.objects.get(group_id=group_id)
    group_members = Vk_api.get_group_members(group_id=group_id, fields="photo_400_orig", offset=group.offset)
    first_indx = 0
    for indx in range(first_indx, len(group_members)):
        try:
            data = group_members[indx]
            data['photo'] = data.pop('photo_400_orig')
            first_indx = indx
            break
        except KeyError:
            pass
    
    for indx in range(first_indx, len(group_members)):
        try:
            data['next_photo'] = group_members[indx]['photo_400_orig']
            break   
        except KeyError:
            pass
    print(data)
    group.offset += 1
    group.save()
    data['offset'] = group.offset
    return data

class VK:
    def __init__(self) -> None:
        self.session = VkApi(token=settings.VK_ACCESS_TOKEN)
        self.vk = self.session.get_api()

    def get_group_members(self, group_id: str, fields: str = "", offset: int = 0):
        return self.vk.groups.getMembers(group_id=group_id, fields=fields, offset=offset)['items']
        
    def get_group_info(self, group_id: str):
        return self.vk.groups.getById(group_id=group_id)[0]


Vk_api = VK()