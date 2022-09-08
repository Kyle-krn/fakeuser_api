from audioop import add
from random import choice
from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework.response import Response
from generators import utils as generator_utils
from datetime import date, timedelta
from . import models
from . import serializers


@api_view(['GET'])
def random_user_view(request):
    host = request.scheme + "://" + request.META['HTTP_HOST']
    gender = request.query_params.get('gender') if request.query_params.get('gender') in ('male', 'female') else choice(('male', 'female'))
    local = request.query_params.get('local') if request.query_params.get('local') in ('ru', 'eng') else choice(('ru', 'eng'))
    photo = choice(models.UserPhoto.objects.filter(gender=gender))
    dob = {
        'age': photo.age,
        'date': date.today() - timedelta(days=365*photo.age)
    }
    photo = {
        'small': host + photo.photo_100.url,
        'medium': host + photo.photo_200.url,
        'original': host + photo.photo.url
    }
    user_data = {'gender': gender,
                 'name': generator_utils.generate_name(count=1, 
                                                       format=0 if local == 'ru' else 6,
                                                       sex=gender)[0],
                 'timezone': generator_utils.generate_timezone(),
                 'location': generator_utils.random_address(localization=local),
                 'email': generator_utils.fake_en.email() if local == 'ru' else generator_utils.fake_ru.email(),
                 'login': generator_utils.random_login(localization=local),
                 'job': generator_utils.random_job(localization=local),
                 'dob': dob,
                 'phone': generator_utils.random_phone_number(localization=local),
                 'photo': photo,
                 'nat': 'Russian' if local == 'ru' else 'American'}

    user_serializer = serializers.RandomUserOutPutSerializer(user_data)
    
    return Response(user_serializer.data)
