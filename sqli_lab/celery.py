import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sqli_lab.settings')

app = Celery('sqli_lab')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()