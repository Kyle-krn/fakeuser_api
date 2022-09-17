"""fake_users_api URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_swagger.views import get_swagger_view
from rest_framework.urlpatterns import format_suffix_patterns
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from generators.views import TemplateView
from django.conf.urls.i18n import i18n_patterns

from generators import views
schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('generators/', include('generators.urls', namespace="generators")),
    # path('parse/', include('parse.urls', namespace="parse")),
    path('api/', include('api.urls', namespace='api')),
    # path('', TemplateView.as_view(template_name="api.html"), name='api_documentation'),
    path('i18/', include('django.conf.urls.i18n'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(), name='swagger-ui'),
]

urlpatterns += i18n_patterns(
    path('', TemplateView.as_view(template_name="api.html"), name='api_documentation'),
    # path('generate_password/', views.TemplateView.as_view(), name="generator_password")
    path('generators/', include('generators.urls', namespace="generators"))

)