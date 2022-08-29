from rest_framework.decorators import api_view
from . import models
from rest_framework.response import Response
from django.views.generic.edit import CreateView
from . import forms
from django.http import HttpRequest
from rest_framework import status
from . import serializers
from django.urls import reverse_lazy


class ParseVkGroupView(CreateView):
    template_name = "photo_parse.html"
    form_class = forms.VkGroupForm
    success_url = reverse_lazy("parse:parse_photo")


@api_view(['GET'])
def get_vk_group_members(request: HttpRequest):
    user_data = models.VkUserRawData.objects.filter(checked=False).order_by('id')[:2]
    if len(user_data) == 0:
        res = Response({'status': 'no data',
                        'count_data': 0})
    else:
        first_obj = user_data[0]
        first_obj.next_photo = user_data[1].photo_url if len(user_data) > 1 else None
        first_obj.count_data = models.VkUserRawData.objects.filter(checked=False).count()
        first_obj.checked = True
        first_obj.save()
        serializer = serializers.VkGroupMemberOutputSerializer(first_obj)
        res = Response(serializer.data)
    res['Access-Control-Allow-Origin'] = '*'
    return res


@api_view(['POST'])
def save_vk_photo(request: HttpRequest):
    serializer = serializers.VkUserSavePhotoSerializer(data=request.data)
    if serializer.is_valid():
        resp = Response({"ok": "ok"})
    else:
        resp = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    resp['Access-Control-Allow-Origin'] = '*'
    return resp