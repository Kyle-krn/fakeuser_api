from django.urls import path
from . import views

app_name = "parse"

urlpatterns = [
    path('parse_photo/', views.TemplateView.as_view()),
    path('vk_group_list/', views.ListVKGroupView.as_view(), name="vk_groups_list"),

    path('get_member_group/<str:group_id>', views.get_vk_group_members),
    path('save_vk_photo/', views.save_vk_photo),

]