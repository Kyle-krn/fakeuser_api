from tokenize import group
from django import forms
from . import models
from . import utils
from django.core.exceptions import ValidationError
from vk_api.exceptions import ApiError

class VkGroupForm(forms.ModelForm):
    def clean_group_id(self):
        data = self.cleaned_data['group_id']
        
        try:
            utils.Vk_api.get_group_info(group_id=data)
        except ApiError:
            raise ValidationError("Group not found!")
        return data

    class Meta:
        model = models.VkGroup
        fields = ["group_id"]
