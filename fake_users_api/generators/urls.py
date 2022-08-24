from django.urls import path
from . import views

urlpatterns = [
    path('generate_password/', views.TemplateView.as_view()),
    path('ajax_password/', views.hello_world),

]