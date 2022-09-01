from django.urls import path
from . import views

app_name = "parse"

urlpatterns = [
    path('parse_photo/', views.ParseVkGroupView.as_view(), name="parse_photo"),
    path('get_member_group/', views.get_vk_group_members),
    path('save_vk_photo/', views.save_vk_photo),

]