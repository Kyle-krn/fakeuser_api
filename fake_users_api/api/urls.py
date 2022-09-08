from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path('', views.random_user_view, name="generator_password"),
]