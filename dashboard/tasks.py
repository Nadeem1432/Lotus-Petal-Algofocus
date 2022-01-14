from __future__ import absolute_import

import requests
import logging
from celery import shared_task

from _lotus_petal.celery import app
# from dashboard.management.commands.get_claas_list import Command
from django.core.management.commands import loaddata
from django.core import management
logger = logging.getLogger(__name__)
logging.basicConfig(filename='tasks.log',filemode='a',format='%(asctime)s-%(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


# @app.task(bind=True)
# def test(self):
#     # print(f'Request: {self.request!r}')
    # print('the task is running')


# @shared_task(name = 'test')
# def test():
#     print('fetching data !!')
    # url = 'https://jsonplaceholder.typicode.com/posts'

    # response = requests.get(url)
    # data = response.json()
    # print(data)


@shared_task(name = 'fetch-class')
def fetch_class_data_classe_365():
    # print('fetching claas data')
    logger.info('fetching claas data')

    management.call_command('get_claas_list')


@shared_task(name = 'fetch-students')
def fetch_students_data_classe_365():
    # print('fetching students data')
    logger.info('fetching students data')

    management.call_command('get_students_data')


@shared_task(name = 'fetch-teachers')
def fetch_teachers_data_classe_365():
    # print('fetching teachers data')
    logger.info('fetching teachers data')

    management.call_command('get_teachers_detail')


@shared_task(name = 'fetch-teachers-zoom-id')
def fetch_teachers_zoom_id():
    # print('fetching teachers zoom id')
    logger.info('fetching teachers zoom id')

    management.call_command('get_teachers_zoom_id')


@shared_task(name = 'update-students-attendance')
def update_students_attendance():
    # print('fetching meetings detail')
    logger.info('fetching meetings detail')

    management.call_command('get_teachers_meeting')


@shared_task(name = 'send-exceptions')
def send_exceptions():
    # print('sending exception....')
    logger.info('sending exception....')

    management.call_command('send_exception_report')



# #===========================================================================
# # code for send mail reports
# from django.shortcuts import HttpResponse
# from dashboard.models import IncorrectTopic
# from attendance.models import StoreOnlineAttendance
# from datetime import date
# import logging
# import os
# from django.conf import settings
#
# # module for csv
# from djqscsv import write_csv , render_to_csv_response
#
# # email send
# from django.core.mail import EmailMessage
#
#
#
# #NOTE: logging config
# # Get an instance of a logger
# logger = logging.getLogger(__name__)
# logging.basicConfig(filename='exception_report.log',
#                     level=logging.ERROR)
#
#
#
# path = f'Reports/{date.today()}'
# incorrect_topic_filename = f'Reports/{date.today()}/Incorrect_Topics.csv'
# wrong_emails_filename = f'Reports/{date.today()}/Wrong_Emails.csv'
#

# def send_reports():
#     try:
#         # create path
#         create_report_path = os.makedirs(os.path.dirname(path), exist_ok=True)
#
#         # get queryset values
#         incorrect_topic_queryset = IncorrectTopic.objects.filter(created_on__date = date.today() ).values()
#         wrong_emails_queryset    = StoreOnlineAttendance.objects.filter(created_at__date = date.today()).values('id',
#                                                                                                                 'uuid',
#
#
#                                                                                                                 'topic_name',
#                                                                                                                 'section_id',
#                                                                                                                 'date',
#                                                                                                                 'wrong_emails',
#                                                                                                                 'created_at')
#
#
#         # write a csv for incorrect topics
#         with open(incorrect_topic_filename, "wb") as csv_file:
#             write_csv(incorrect_topic_queryset, csv_file)
#
#         # write a csv for incorrect topics
#         with open(wrong_emails_filename, "wb") as csv_file:
#             write_csv(wrong_emails_queryset, csv_file)
#
#
#         try:
#
#             # email body
#             msg = EmailMessage(f'Exception Report {date.today()}',
#                                 f'Dear Admin ,\nPlease find the attached exception reports for Incorrect\
#                                     Topics and Wrong emails for student on login for the {date.today()} .\
#                                         \n\nRegards ,\nStudywell Team',
#                                 settings.EMAIL_HOST_USER,
#                                 ['sumeet@stackfusion.io','nadeem.ali@stackfusion.io','ravinder.kumar@stackfusion.io','rajat.p@lotuspetalfoundation.org'])
#
#             msg.attach_file(f'Reports/{date.today()}/Incorrect_Topics.csv' )
#             msg.attach_file(f'Reports/{date.today()}/Wrong_Emails.csv')
#             msg.send()
#
#             logging.info("exception reports mail successfully sent...")
#             print('exception reports successfully sent...')
#
#         except Exception as e:
#             print(f"Error : {e}")
#             logging.error(f"Error : {e}")
#
#
#     except Exception as e:
#         print(f'Error : {e}...')
#         logging.error(f"Error : {e}")
