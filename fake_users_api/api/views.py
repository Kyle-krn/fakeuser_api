from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework_yaml.renderers import YAMLRenderer
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from generators import utils as generator_utils
from generators.utils import NATIONALITY, USER_ACCEPT_FIELDS
from faker import Faker
import random
from . import serializers
from . import models


@extend_schema(
        parameters=[
          serializers.UserRequestSerialzer,
        ],
        request=serializers.UserRequestSerialzer,
        responses=serializers.UserResponseSerializer,
    )
class ApiView(APIView):
    renderer_classes = JSONRenderer, BrowsableAPIRenderer, XMLRenderer, YAMLRenderer
    serializer_class = serializers.UserResponseSerializer

    def get_query_params(self):
        serializer = serializers.UserRequestSerialzer(data={
            'gender' : self.request.query_params.get('gender'),
            'local' : [i.strip() for i in self.request.query_params.get('local').split(',') if i.strip() in NATIONALITY] if self.request.query_params.get('local') else ['us'],
            'include' : [i.strip() for i in self.request.query_params.get('include').split(',') if i.strip() in USER_ACCEPT_FIELDS] if self.request.query_params.get('include') else USER_ACCEPT_FIELDS,
            'exclude' : [i.strip() for i in self.request.query_params.get('exclude').split(',') if i.strip() in USER_ACCEPT_FIELDS] if self.request.query_params.get('exclude') else [],
            'count' : self.request.query_params.get('count') if self.request.query_params.get('count', '').isdigit() else 1,
            'seed' : self.request.query_params.get('seed')
        })
        serializer.is_valid()
        return serializer.data
 
    def get(self, request, format=None):
        params = self.get_query_params()
        return_fields = [field for field in params['include'] if field not in params['exclude']]
        print(return_fields)
        faker = Faker(['ru_RU', 'en_US', 'az_AZ', 'bn_BD', 'cs_CZ', 'da_DK', 'de_DE', 'el_GR', 'es_CL'])
        faker.seed_instance(params['seed'])
        random.seed(params['seed'])
        photo_models_male,photo_models_female  = models.UserPhoto.objects.filter(gender='male'), models.UserPhoto.objects.filter(gender='female')
        data = {
            'count': params['count'],
            'results': [generator_utils.RandomUser(gender=params['gender'],
                                                   photo_models=(photo_models_male,photo_models_female), 
                                                   localization=random.choice(list(params['local'])), 
                                                   return_fields=return_fields,
                                                   user_faker=faker).return_dict()],
            'seed': params['seed']
        }
        serializer = self.serializer_class(data=data)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK, headers={'Access-Control-Allow-Origin': '*'})