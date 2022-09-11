from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "api"

urlpatterns = [
    path('', views.random_user_view, name="generator_password"),
]

