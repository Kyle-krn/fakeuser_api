from statistics import mode
from django.contrib import admin
from . import models


@admin.register(models.VkGroup)
class VkGroupAdmin(admin.ModelAdmin):
    pass