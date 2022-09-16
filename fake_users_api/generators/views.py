from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views import generic
from rest_framework import status
import uuid
from . import serializers
from . import utils


class TemplateView(generic.TemplateView):
    template_name = "password.html"


@api_view(['GET'])
def generate_password_ajax(request):
    serializer = serializers.PasswordInputSerializer(data = {
        'length': request.query_params.get('lenght'),
        'easy_to_read': request.query_params.get('easy_to_read', 0),
        'characters': request.query_params.getlist('characters', [])
    })
    if serializer.is_valid():
        password = utils.generate_password(length=serializer.data["length"],
                                           easy_to_read=serializer.data["easy_to_read"],
                                           characters=serializer.data["characters"])
        return Response({"password": password}, status=status.HTTP_200_OK, headers={'Access-Control-Allow-Origin': '*'})
    else:
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, headers={'Access-Control-Allow-Origin': '*'})


@api_view(['POST'])
def generate_name_ajax(request):
    serializer = serializers.NameInputSerializer(data=request.data)
    if serializer.is_valid():
        names = utils.generate_name(count=serializer.data['count'], format=serializer.data['format'], sex=serializer.data['sex'])
        return Response({"count": serializer.data['count'], "names": names}, status=status.HTTP_200_OK, headers={'Access-Control-Allow-Origin': '*'})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, headers={'Access-Control-Allow-Origin': '*'})


@api_view(['GET'])
def generate_uuid_ajax(request):
    count = int(request.query_params.get('count')) if request.query_params.get('count') and request.query_params.get('count').isdigit() else 1
    version = int(request.query_params.get('version')) if request.query_params.get('version') and request.query_params.get('version') in ('1', '4') else 4
    results = [uuid.uuid1() if version == 1 else uuid.uuid4() for i in range(count)]
    return Response({'count': count, 'version': version, 'results': results}, status=status.HTTP_200_OK, headers={'Access-Control-Allow-Origin': '*'})
    