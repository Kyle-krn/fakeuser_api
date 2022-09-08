from celery import shared_task
from . import models
from . import utils
from api import models as api_models
import cv2
import os
import requests
from bs4 import BeautifulSoup
from typing import Literal

@shared_task
def parse_user_info(group_id: str):  
    offset = 0
    group_members_info = utils.Vk_api.get_group_members(group_id=group_id, fields="photo_400_orig", offset=offset)
    while len(group_members_info) > 0:
        for member in group_members_info:
            # print(member)
            if "photo_400_orig" not in member:
                continue
            # print(member['photo_400_orig'])
            img = utils.get_avatar(member['photo_400_orig'])
            if img is None:
                continue
            count = api_models.UserPhoto.objects.all().count()

            try:
                img_100 = cv2.resize(img, (100,100))
                img_200 = cv2.resize(img, (200,200))
            except cv2.error:
                continue

            img_path = f"media/images/photo/{count+1}.jpg"
            img_100_path = f"media/images/photo_100/{count+1}.jpg"
            img_200_path = f"media/images/photo_200/{count+1}.jpg"
            
            cv2.imwrite(img_path, img)
            cv2.imwrite(img_200_path, img_200)
            cv2.imwrite(img_100_path, img_100)

            analyze = utils.face_analyze(img_path)
            if isinstance(analyze, dict) is False:
                os.remove(img_path)
                os.remove(img_100_path)
                os.remove(img_200_path)
                continue

            api_models.UserPhoto.objects.create(photo_100="/".join(img_100_path.split('/')[1:]),
                                                photo_200="/".join(img_200_path.split('/')[1:]),
                                                photo="/".join(img_path.split('/')[1:]),
                                                age=analyze['age'],
                                                gender='male' if analyze['gender'].lower() == 'man' else 'female')
        offset += len(group_members_info)
        group_members_info = utils.Vk_api.get_group_members(group_id=group_id, fields="photo_400_orig", offset=offset)


@shared_task
def parse_name(lang: Literal['ru', 'eng'], gender: Literal['man', 'woman']):
    if lang == 'ru':
        lang_type = 0
    else:
        lang_type = 101
    
    if gender == 'man':
        sex = 0
    if gender == 'woman':
        sex = 1
    url = "https://randomus.ru/name"
    params = {"type": lang_type, "sex": sex, "count": 100}
    
    for i in range(0, 10):
        resp = requests.get(url=url, params=params)
        soup = BeautifulSoup(resp.text, "lxml")
        results = soup.find("div", id='result_tiles').find_all("div", {'class': 'control'})

        for result in results:
            result = result.find('span').text.split(" ")
            name = api_models.UserName()
            
            if lang == 'eng':
                name.first_name = result[0] if len(api_models.UserName.objects.filter(first_name=result[0])) == 0 else None
                name.last_name = result[1] if len(api_models.UserName.objects.filter(last_name=result[1])) == 0 else None
            else:
                name.first_name = result[1] if len(api_models.UserName.objects.filter(first_name=result[1])) == 0 else None
                name.last_name = result[0] if len(api_models.UserName.objects.filter(last_name=result[0])) == 0 else None
                name.patronymic = result[2] if len(api_models.UserName.objects.filter(patronymic=result[2])) == 0 else None

            if name.first_name is None and name.last_name is None and name.patronymic is None:
                continue

            name.gender = gender
            name.localization = lang
            name.save()
        



