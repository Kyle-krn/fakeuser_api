from django.urls import path
from . import views

urlpatterns = [
    path('parse_photo/', views.TemplateView.as_view()),
    path('get_member_group/', views.get_vk_group_members),

]