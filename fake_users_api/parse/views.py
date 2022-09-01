from rest_framework.decorators import api_view
from . import models
from rest_framework.response import Response
from django.views.generic.edit import CreateView
from . import forms
from django.http import HttpRequest
from rest_framework import status
from . import serializers
from django.urls import reverse_lazy
from api import models as api_models
import requests
from tempfile import NamedTemporaryFile
from django.core.files import File
from PIL import Image
from io import BytesIO

class ParseVkGroupView(CreateView):
    template_name = "photo_parse.html"
    form_class = forms.VkGroupForm
    success_url = reverse_lazy("parse:parse_photo")


# @api_view(['GET'])
# def get_vk_group_members(request: HttpRequest):
#     user_data = models.VkUserRawData.objects.filter(checked=False).order_by('id')[:2]
#     if len(user_data) == 0:
#         res = Response({'status': 'no data',
#                         'count_data': 0})
#     else:
#         first_obj = user_data[0]
#         first_obj.next_photo = user_data[1].photo_400 if len(user_data) > 1 else None
#         first_obj.count_data = models.VkUserRawData.objects.filter(checked=False).count()
#         first_obj.checked = True
#         first_obj.save()
#         serializer = serializers.VkGroupMemberOutputSerializer(first_obj)
#         res = Response(serializer.data)
#     res['Access-Control-Allow-Origin'] = '*'
#     return res


# @api_view(['POST'])
# def save_vk_photo(request: HttpRequest):
#     serializer = serializers.VkUserSavePhotoSerializer(data=request.data)
#     if serializer.is_valid():
#         data = serializer.validated_data
#         raw_user = models.VkUserRawData.objects.get(user_id=data['user_id'])
#         raw_user.saved = True
#         raw_user.save()
#         photo_user = api_models.UserPhoto()
#         photo_user.gender = data['gender']
#         r = requests.get(raw_user.photo_400)
#         img_temp = NamedTemporaryFile(delete=True)
#         img_temp.write(r.content)
#         img_temp.flush()
#         img_orig = Image.open(img_temp)
#         img_200 = img_orig.resize((200,200))
#         img_100 = img_orig.resize((100,100))
#         blob_400 = BytesIO()
#         img_orig.save(blob_400, 'JPEG')
#         blob_200 = BytesIO()
#         img_200.save(blob_200, 'JPEG')
#         blob_100 = BytesIO()
#         img_100.save(blob_100, 'JPEG')
#         photo_user.photo_400.save(f"{data['user_id']}.jpg", File(blob_400)  , save=True)
#         photo_user.photo_200.save(f"{data['user_id']}.jpg", File(blob_200)  , save=True)
#         photo_user.photo_100.save(f"{data['user_id']}.jpg", File(blob_100)  , save=True)
#         photo_user.save() 
#         resp = Response({"ok": "ok"})
#     else:
#         resp = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     resp['Access-Control-Allow-Origin'] = '*'
#     return resp
