from django.urls import path
from . import views

app_name = "generators"

urlpatterns = [
    path('generate_password/', views.TemplateView.as_view(), name="generator_password"),
    path('ajax_password/', views.generate_password_ajax, name="ajax_password"),
    path('ajax_name/', views.generate_name_ajax, name="ajax_name"),

]