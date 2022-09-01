from typing import Union
from vk_api import VkApi
from django.conf import settings
from deepface import DeepFace 
import cv2
import urllib
import numpy as np


class VK:
    def __init__(self) -> None:
        self.session = VkApi(token=settings.VK_ACCESS_TOKEN)
        self.vk = self.session.get_api()

    def get_group_members(self, group_id: str, fields: str = "", offset: int = 0) -> dict:
        return self.vk.groups.getMembers(group_id=group_id, fields=fields, offset=offset)['items']
        
    def get_group_info(self, group_id: str) -> dict:
        return self.vk.groups.getById(group_id=group_id)[0]


def url_to_image(url: str) -> np.ndarray:
    with urllib.request.urlopen(url) as url:
        image = np.asarray(bytearray(url.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.COLOR_BGR2GRAY)
    return image


def get_avatar(url) -> Union[None, np.ndarray]:
    img = url_to_image(url)
    faces = cv2.CascadeClassifier("faces.xml")
    results = faces.detectMultiScale(img, minNeighbors=3, scaleFactor=2)

    if len(results) != 1 or len(img) == 0:
        return

    for (x, y, w, h) in results:
        # img = img[y:y + (h), x:x + (w)]
        img = img[y-50:y + (h+50), x-50:x + (w+50)]
    if len(img) == 0:
        return
    return img


def face_analyze(path):
    try:
        result = DeepFace.analyze(img_path=path, actions=['age', 'gender'])
        return result
    except Exception as _exc:
        return _exc

Vk_api = VK()

