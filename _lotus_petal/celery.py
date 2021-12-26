from __future__ import absolute_import

import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_lotus_petal.settings')

app = Celery('_lotus_petal')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()



app.conf.beat_schedule = {
    # 'fetch-class-data': {
    #     'task': 'fetch-class',
    #     'schedule': crontab(hour=21),
    # },
    # 'fetch-students-data': {
    #     'task': 'fetch-students',
    #     'schedule': crontab(hour=21, minute=30),
    # },
    # 'fetch-teachers-data': {
    #     'task': 'fetch-teachers',
    #     'schedule': crontab(hour=21, minute=10),
    # },
    # 'fetch-teachers-zoom-id': {
    #     'task': 'fetch-teachers-zoom-id',
    #     'schedule': crontab(hour=21, minute=20),
    # },
    # 'update-students-attendance': {
    #     'task': 'update-students-attendance',
    #     'schedule': crontab(hour=22),
    # },
    # 'mark-offline-attendance': {
    #     'task': 'mark-offline-attendance',
    #     'schedule': crontab(hour = 23)
    # },

    #task for send daily exception report
    'send-exceptions-report': {
        'task': 'send-exceptions',
        'schedule': crontab(hour=22, minute=30),
    }
    

}