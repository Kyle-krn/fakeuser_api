from django.urls import path
from . import views

app_name = "parse"

urlpatterns = [
    path('parse_photo/', views.ParseVkGroupView.as_view(), name="parse_photo"),
]