from random import choice
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from generators import utils as generator_utils
from .render import UserCsvRender
from django.http import HttpRequest
from . import serializers
from rest_framework import status
from rest_framework.renderers import JSONRenderer


@api_view(['GET'])
@renderer_classes((JSONRenderer, UserCsvRender))
def random_user_view(request: HttpRequest):
    gender = request.query_params.get('gender')
    local = request.query_params.get('local') if request.query_params.get('local') in ('ru', 'eng') else choice(('ru', 'eng'))
    include = [i.strip() for i in request.query_params.get('include').split(',')] if request.query_params.get('include') else []
    exclude = [i.strip() for i in request.query_params.get('exclude').split(',')] if request.query_params.get('exclude') else []
    count = int(request.query_params.get('count')) if request.query_params.get('count') and request.query_params.get('count').isdigit() else 1
    if count < 1: count = 1
    data = {
        'count': count,
        'results': [generator_utils.RandomUser(gender=gender, localization=local).return_dict(include=include, exclude=exclude) for i in range(count)]
    }
    serializer = serializers.UserResponseSerializer(data=data)
    if serializer.is_valid():
        resp = Response(serializer.data, status=status.HTTP_200_OK)
        resp['Access-Control-Allow-Origin'] = '*'
        return resp
