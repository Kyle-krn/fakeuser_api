from django.db import models

GENDER = (
    ("man", "man"),
    ("woman", "woman"),
)

LANG_NAME = (
    ("ru", "ru"),
    ("eng","eng")
)

class UserPhoto(models.Model):
    photo_100 = models.ImageField(upload_to='images/photo_100/')
    photo_200 = models.ImageField(upload_to='images/photo_200/')
    photo = models.ImageField(upload_to='images/photo/')
    gender = models.CharField(max_length=7, choices=GENDER, null=True)
    age = models.IntegerField(null=True)

    class Meta:
        db_table = "user_photo"


class UserName(models.Model):
    first_name = models.CharField(max_length=255, unique=True, null=True)
    last_name = models.CharField(max_length=255, unique=True, null=True)
    patronymic = models.CharField(max_length=255, unique=True, null=True)
    gender = models.CharField(max_length=255, choices=GENDER)
    localization = models.CharField(max_length=40, choices=LANG_NAME)

    class Meta:
        db_table = 'user_name'