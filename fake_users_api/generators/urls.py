from django.urls import path
from . import views

app_name = "generators"

urlpatterns = [
    path('generate_password/', views.TemplateView.as_view(), name="generator_password"),
    path('ajax_password/', views.hello_world, name="ajax_password"),

]