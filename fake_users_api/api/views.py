from random import choice
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from generators import utils as generator_utils
from .render import UserCsvRender
from django.http import HttpRequest
from . import serializers
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework_yaml.renderers import YAMLRenderer


@api_view(['GET'])
@renderer_classes((JSONRenderer, XMLRenderer, YAMLRenderer, UserCsvRender))
def random_user_view(request: HttpRequest):
    gender = request.query_params.get('gender')
    local = request.query_params.get('local')
    include = [i.strip() for i in request.query_params.get('include').split(',')] if request.query_params.get('include') else []
    exclude = [i.strip() for i in request.query_params.get('exclude').split(',')] if request.query_params.get('exclude') else []
    count = int(request.query_params.get('count')) if request.query_params.get('count') and request.query_params.get('count').isdigit() else 1
    seed = request.query_params.get('seed')
    if count < 1: count = 1
    if count > 100: count = 100
    data = {
        'count': count,
        'results': [generator_utils.RandomUser(gender=gender, localization=local, seed=seed).return_dict(include=include, exclude=exclude) for i in range(count)]
    }
    serializer = serializers.UserResponseSerializer(data=data)
    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK, headers={'Access-Control-Allow-Origin': '*'})
    print(serializer.errors)
    resp = Response({"ok": False}, status=status.HTTP_200_OK)
    resp['Access-Control-Allow-Origin'] = '*'
    return resp
