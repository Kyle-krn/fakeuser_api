from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework_yaml.renderers import YAMLRenderer
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from generators import utils as generator_utils
from faker import Faker
import random
from . import serializers


@extend_schema(
        parameters=[
          serializers.UserRequestSerialzer,
        ],
        request=serializers.UserRequestSerialzer,
        responses=serializers.UserResponseSerializer,
    )
class ApiView(APIView):
    renderer_classes = JSONRenderer,TemplateHTMLRenderer, BrowsableAPIRenderer, XMLRenderer, YAMLRenderer
    serializer_class = serializers.UserResponseSerializer
    template_name = 'api.html'

    def get_query_params(self):
        gender = self.request.query_params.get('gender')
        local = [i.strip() for i in self.request.query_params.get('local').split(',')] if self.request.query_params.get('local') else ['us']
        include = [i.strip() for i in self.request.query_params.get('include').split(',')] if self.request.query_params.get('include') else []
        exclude = [i.strip() for i in self.request.query_params.get('exclude').split(',')] if self.request.query_params.get('exclude') else []
        count = int(self.request.query_params.get('count')) if self.request.query_params.get('count') and self.request.query_params.get('count').isdigit() else 1
        seed = self.request.query_params.get('seed') if  self.request.query_params.get('seed') else generator_utils.generate_password(length=15)
        if count < 1: count = 1
        if count > 100: count = 100
        return gender, local, include, exclude, count, seed
 
    def get(self, request, format=None):
        gender, local, include, exclude, count, seed = self.get_query_params()
        print(format)
        faker = Faker(['ru_RU', 'en_US', 'az_AZ', 'bn_BD', 'cs_CZ', 'da_DK', 'de_DE', 'el_GR', 'es_CL'])
        faker.seed_instance(seed)
        random.seed(seed)
        data = {
            'count': count,
            'results': [generator_utils.RandomUser(gender=gender, localization=random.choice(local), user_faker=faker).return_dict(include=include, exclude=exclude) for i in range(count)],
            'seed': seed
        }
        serializer = self.serializer_class(data=data)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK, headers={'Access-Control-Allow-Origin': '*'})


# not snn: da_DK, 