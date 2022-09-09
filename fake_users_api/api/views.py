import imp
from random import choice
from rest_framework.decorators import api_view
from rest_framework.response import Response
from generators import utils as generator_utils
from django.http import HttpRequest
from . import serializers


@api_view(['GET'])
def random_user_view(request: HttpRequest):
    host = request.scheme + "://" + request.META['HTTP_HOST']
    gender = request.query_params.get('gender') if request.query_params.get('gender') in ('male', 'female') else choice(('male', 'female'))
    local = request.query_params.get('local') if request.query_params.get('local') in ('ru', 'eng') else choice(('ru', 'eng'))
    include = [i.strip() for i in request.query_params.get('include').split(',')] if request.query_params.get('include') else []
    exclude = [i.strip() for i in request.query_params.get('exclude').split(',')] if request.query_params.get('exclude') else []
    user = generator_utils.RandomUser(gender=gender, localization=local)
    resp = Response(user.return_dict(include=include, exclude=exclude))
    resp['Access-Control-Allow-Origin'] = '*'
    return resp