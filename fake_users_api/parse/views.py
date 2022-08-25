from django.shortcuts import render
from django.views import generic
from rest_framework.decorators import api_view
from . import utils
from rest_framework.response import Response

class TemplateView(generic.TemplateView):
    template_name = "photo_parse.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@api_view(['GET'])
def get_vk_group_members(request):
    res = {
        "photo": utils.get_group_members()['items'][0]["photo_max_orig"],
        "first_name": utils.get_group_members()['items'][0]["first_name"],
        "last_name": utils.get_group_members()['items'][0]["last_name"],
        "next_photo": utils.get_group_members()['items'][1]["photo_max_orig"],
    }
    return Response(res)