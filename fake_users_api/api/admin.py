from statistics import mode
from django.contrib import admin
from . import models


@admin.register(models.UserPhoto)
class PhotoAdmin(admin.ModelAdmin):
    list_filter = ('gender', 'age') 

