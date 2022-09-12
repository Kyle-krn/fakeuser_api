from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework_yaml.renderers import YAMLRenderer
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from generators import utils as generator_utils
from . import serializers

@extend_schema(
        parameters=[
          serializers.UserRequestSerialzer,
        ],
        request=serializers.UserRequestSerialzer,
        responses=serializers.UserResponseSerializer,
    )
class ListUsers(APIView):
    renderer_classes = JSONRenderer, BrowsableAPIRenderer, XMLRenderer, YAMLRenderer
    serializer_class = serializers.UserResponseSerializer

    def get_query_params(self):
        gender = self.request.query_params.get('gender')
        local = self.request.query_params.get('local')
        include = [i.strip() for i in self.request.query_params.get('include').split(',')] if self.request.query_params.get('include') else []
        exclude = [i.strip() for i in self.request.query_params.get('exclude').split(',')] if self.request.query_params.get('exclude') else []
        count = int(self.request.query_params.get('count')) if self.request.query_params.get('count') and self.request.query_params.get('count').isdigit() else 1
        seed = self.request.query_params.get('seed')
        return gender, local, include, exclude, count, seed
 
    def get(self, request, format=None):
        gender, local, include, exclude, count, seed = self.get_query_params()
        if count < 1: count = 1
        if count > 100: count = 100
        data = {
            'count': count,
            'results': [generator_utils.RandomUser(gender=gender, localization=local, seed=seed).return_dict(include=include, exclude=exclude) for i in range(count)]
        }
        serializer = self.serializer_class(data=data)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK, headers={'Access-Control-Allow-Origin': '*'})