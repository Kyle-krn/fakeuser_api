from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views import generic
from rest_framework import status
from . import serializers
from . import utils


class TemplateView(generic.TemplateView):
    template_name = "password.html"


@api_view(['POST'])
def generate_password_ajax(request):
    serializer = serializers.PasswordInputSerializer(data=request.data)
    if serializer.is_valid():
        password = utils.generate_password(length=serializer.data["password_length"],
                                           easy_to_read=serializer.data["easy_to_read"],
                                           characters=serializer.data["characters"])
        resp = Response({"password": password}, status=status.HTTP_200_OK)
    else:
        resp = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    resp['Access-Control-Allow-Origin'] = '*'
    return resp


@api_view(['POST'])
def generate_name_ajax(request):
    serializer = serializers.NameInputSerializer(data=request.data)
    if serializer.is_valid():
        names = utils.generate_name(count=serializer.data['count'], format=serializer.data['format'], sex=serializer.data['sex'])
        resp = Response({"count": serializer.data['count'], "names": names}, status=status.HTTP_200_OK)
    else:
        resp = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    resp['Access-Control-Allow-Origin'] = '*'
    return resp

