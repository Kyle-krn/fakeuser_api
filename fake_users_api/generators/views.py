from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views import generic
from drf_spectacular.utils import extend_schema
from rest_framework import status
import uuid
from . import serializers
from . import utils


class TemplateView(generic.TemplateView):
    template_name = "password.html"

@extend_schema(
        parameters=[
          serializers.PasswordInputSerializer,
        ],
        request=serializers.PasswordInputSerializer,
        responses=serializers.PasswordOutPutSerializer,
    )
@api_view(['GET'])
def generate_password_ajax(request):
    '''
        Представление генерации пароля
    '''
    print(request.query_params.get('length'))
    serializer = serializers.PasswordInputSerializer(data = {
        'length': request.query_params.get('length'),
        'easy_to_read': request.query_params.get('easy_to_read'),
        'characters': request.query_params.getlist('characters')
    })
    if serializer.is_valid():
        password = utils.generate_password(length=serializer.data["length"],
                                           easy_to_read=serializer.data["easy_to_read"],
                                           characters=serializer.data["characters"])
        output_serializer = serializers.PasswordOutPutSerializer(data = {'password': password})
        output_serializer.is_valid()
        return Response(output_serializer.data, status=status.HTTP_200_OK, headers={'Access-Control-Allow-Origin': '*'})
    else:
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, headers={'Access-Control-Allow-Origin': '*'})


@extend_schema(
        parameters=[
          serializers.NameInputSerializer,
        ],
        request=serializers.NameInputSerializer,
        responses=serializers.NameOutPutSerializer,
    )
@api_view(['GET'])
def generate_name_ajax(request):
    '''
        Представление генерации имени
    '''
    serializer = serializers.NameInputSerializer(data={
        'count': request.query_params.get('count'),
        'lang': request.query_params.get('lang'),
        'sex': request.query_params.get('sex'),
    })
    if serializer.is_valid():
        names = utils.generate_name(count=serializer.data['count'], lang=serializer.data['lang'], sex=serializer.data['sex'])
        output_serialzier = serializers.NameOutPutSerializer(data={'count': serializer.data['count'], "names":names})
        output_serialzier.is_valid()
        return Response(output_serialzier.data, status=status.HTTP_200_OK, headers={'Access-Control-Allow-Origin': '*'})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, headers={'Access-Control-Allow-Origin': '*'})


@extend_schema(
        parameters=[
          serializers.UUIDInputSerializer,
        ],
        request=serializers.UUIDInputSerializer,
        responses=serializers.UUIDOutPutSerializer,
    )
@api_view(['GET'])
def generate_uuid_ajax(request):
    '''
        Представление генерации UUID
    '''
    serializer = serializers.UUIDInputSerializer(data = {
        'count': request.query_params.get('count'),
        'version': request.query_params.get('version')          
    })
    if serializer.is_valid():
        output_serializer = serializers.UUIDOutPutSerializer(data = {
            'count': serializer.data['count'],    
            'version': serializer.data['version'],    
            'results': [uuid.uuid1() if serializer.data['version'] == 1 else uuid.uuid4() for i in range(serializer.data['count'])],    
        })
        output_serializer.is_valid()
        return Response(output_serializer.data, status=status.HTTP_200_OK, headers={'Access-Control-Allow-Origin': '*'})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, headers={'Access-Control-Allow-Origin': '*'})