from __future__ import absolute_import, unicode_literals
import os
import configurations
from celery import Celery
from celery.schedules import crontab

if not ("DJANGO_SETTINGS_MODULE" in os.environ):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')

configurations.setup()
app = Celery('financial')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-news-task': {
        'task': 'app.financial.tasks.update_news',
        'schedule': crontab(minute=0, hour=0),
    },
}