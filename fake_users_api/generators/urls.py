from django.urls import path
from . import views

app_name = "generators"

urlpatterns = [
    path('generate_password/', views.TemplateView.as_view(), name="generator_password"),
    path('generate_name/', views.TemplateView.as_view(template_name="name.html"), name="generator_name"),
    path('generate_uuid/', views.TemplateView.as_view(template_name="uuid.html"), name="generator_uuid"),
    path('ajax_password/', views.generate_password_ajax, name="ajax_password"),
    path('ajax_name/', views.generate_name_ajax, name="ajax_name"),
    path('ajax_uuid/', views.generate_uuid_ajax, name="ajax_uud"),

]