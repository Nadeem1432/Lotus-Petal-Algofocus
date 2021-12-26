from __future__ import absolute_import
import logging
from celery import shared_task
from django.core import management
from django.core.management.commands import loaddata

from _lotus_petal.celery import app


logger = logging.getLogger(__name__)

logging.basicConfig(format='%(asctime)s-%(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


@shared_task(name = 'mark-offline-attendance')
def mark_offline_attendance():
    logger.info('Starting offline attendance marking')

    management.call_command('mark_offline_attendance')