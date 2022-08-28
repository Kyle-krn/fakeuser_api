from statistics import mode
from django.shortcuts import render
from django.views import generic
from rest_framework.decorators import api_view
from . import models
from rest_framework.response import Response
from django.views.generic import ListView
from django.views.generic.edit import BaseCreateView
from . import forms
from django.http import HttpRequest
from rest_framework import status
from . import serializers


class TemplateView(generic.TemplateView):
    template_name = "photo_parse.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ListVKGroupView(BaseCreateView, ListView):
    template_name = "list_vk_group.html"
    model = models.VkGroup
    context_object_name = "groups"
    form_class = forms.VkGroupForm
    object_list = models.VkGroup.objects.all()
    paginate_by = 1



@api_view(['GET'])
def get_vk_group_members(request: HttpRequest, group_id: str):
    group = models.VkGroup.objects.get(group_id=group_id)
    user_data = models.VkUserRawData.objects.filter(group_id=group.id, 
                                                    checked=False).order_by('id')[:2]
    first_obj = user_data[0]
    first_obj.next_photo = user_data[1].photo_url

    first_obj.checked = True
    first_obj.save()
    serializer = serializers.VkGroupMemberOutputSerializer(first_obj)
    return Response(serializer.data)


@api_view(['POST'])
def save_vk_photo(request: HttpRequest):
    serializer = serializers.VkUserSavePhotoSerializer(data=request.data)
    if serializer.is_valid():
        resp = Response({"ok": "ok"})
    else:
        resp = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    resp['Access-Control-Allow-Origin'] = '*'
    return resp