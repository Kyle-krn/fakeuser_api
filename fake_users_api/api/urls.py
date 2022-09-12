from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

app_name = "api"

urlpatterns = [
    # path('', views.random_user_view, name="generator_password"),
    path('', views.ListUsers.as_view(), name="random_user"),
]

# urlpatterns += [

# ]