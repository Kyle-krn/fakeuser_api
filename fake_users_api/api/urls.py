from django.urls import path
from . import views


app_name = "api"


urlpatterns = [
    path('', views.ApiView.as_view(), name="random_user"),
]