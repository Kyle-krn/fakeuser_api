from rest_framework import serializers
from . import models

class VkGroupMemberOutputSerializer(serializers.ModelSerializer):
    next_photo = serializers.URLField(allow_null=True)
    count_data = serializers.IntegerField()
    class Meta:
        model = models.VkUserRawData
        fields = ['user_id', 'first_name', 'last_name', 'photo_url', 'next_photo', 'count_data']


class VkUserSavePhotoSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    gender = serializers.ChoiceField(choices=('female', 'male'))

    def validate_user_id(self, value):
        try:
            models.VkUserRawData.objects.get(user_id=value)
        except models.VkUserRawData.DoesNotExist:
            raise serializers.ValidationError("User does not exist")