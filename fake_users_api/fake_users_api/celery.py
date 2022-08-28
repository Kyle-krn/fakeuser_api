import os  
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fake_users_api.settings')
celery_app = Celery('fake_users_api')  
celery_app.config_from_object('django.conf:settings', namespace='CELERY')  
celery_app.autodiscover_tasks()