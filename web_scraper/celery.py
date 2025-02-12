from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set default Django settings module for 'celery'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_scraper.settings')

app = Celery('web_scraper')

# Load settings from Django settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

broker_connection_retry_on_startup = True
app.conf.update(
    worker_concurrency=1,  # Solo pool allows only one task to be processed at a time
    worker_pool='solo'  # Ensure solo pool is used on Windows
)

# Autodiscover tasks.py files in installed apps
app.autodiscover_tasks()

