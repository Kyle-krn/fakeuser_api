from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from . import models
from generators.utils import USER_ACCEPT_FIELDS
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

class RandomUserTest(APITestCase):
    url = reverse('api:random_user')

    def setUp(self):
        models.UserPhoto.objects.create(photo_100='images/photo_100/1.jpg',
                                        photo_200='images/photo_200/1.jpg',
                                        photo='images/photo/1.jpg',
                                        gender='male',
                                        age=20)
        models.UserPhoto.objects.create(photo_100='images/photo_100/2.jpg',
                                        photo_200='images/photo_200/2.jpg',
                                        photo='images/photo/2.jpg',
                                        gender='female',
                                        age=20)
        models.UserPhoto.objects.create(photo_100='images/photo_100/3.jpg',
                                        photo_200='images/photo_200/3.jpg',
                                        photo='images/photo/3.jpg',
                                        gender='male',
                                        age=20)
        models.UserPhoto.objects.create(photo_100='images/photo_100/4.jpg',
                                        photo_200='images/photo_200/4.jpg',
                                        photo='images/photo/4.jpg',
                                        gender='female',
                                        age=20)

    def test_random_gender_and_include(self):
        data = {'gender': 'male', 'include': 'gender'}
        response = self.client.get(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['results'][0]['gender'], data['gender'])
        self.assertEqual(list(response.json()['results'][0].keys()), [data['include']])

    def test_random_exclude(self):
        data = {'exclude': 'photo'}
        include = [i for i in USER_ACCEPT_FIELDS if i != 'photo']
        response = self.client.get(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response.json()['results'][0].keys()), include)

    def test_random_seed(self):
        data = {'seed': 'foobar', 'exclude': 'photo, dob'}
        output_try_data = {
            "gender": "male",
            "name": {
                "title": "Mr.",
                "first_name": "David",
                "last_name": "Bailey",
                "patronymic": None
            },
            "timezone": {
                "offset": "-07:00",
                "description": "America/Los_Angeles"
            },
            "location": {
                "street": "Melissa Views",
                "house": "300",
                "city": "Stokesshire",
                "state": "Oregon",
                "country": "United States",
                "postcode": 53448,
                "coordinates": {
                    "lat": 33.7207,
                    "long": -116.21677
                }
            },
            "email": "usmith@example.net",
            "login": {
                "uuid": "e156ed2c-81fd-442a-a2b2-82630807e45d",
                "username": "xschmitt",
                "password": "sU*|cHA6",
                "md5": "0e7979eb2fc7164f627371f9f2349805",
                "sha1": "41ece2df076198424eaef3139699ec5990619def",
                "sha256": "b3a21ddb1396fc8833862b01fada920564e8e5c965c230b345aa8c706ef483dc"
            },
            "job": {
                "job": "Heritage manager",
                "company": "Woods LLC"
            },
            "registered": {
                "date": "2021-11-07T01:31:09.347066Z",
                "days": 315
            },
            "phone": "+17729676069",
            "nat": "American",
            "ssn": "182-73-9344"
        }
        response = self.client.get(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['results'][0], output_try_data)
        
    def test_local(self):
        data = {'local': 'ru', 'include': 'nat'}
        response = self.client.get(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['results'][0]['nat'], 'Russian')
    