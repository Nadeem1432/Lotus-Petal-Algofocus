
from django.core.management.base import BaseCommand
#===========================================================================
# code for send mail reports
from django.shortcuts import HttpResponse
from dashboard.models import IncorrectTopic
from attendance.models import StoreOnlineAttendance
from datetime import date
import logging
import os
from django.conf import settings

# module for csv
from djqscsv import write_csv , render_to_csv_response

# email send
from django.core.mail import EmailMessage
from pathlib import Path

#NOTE: logging config
# Get an instance of a logger
logger = logging.getLogger(__name__)
logging.basicConfig(filename='exception_report.log',filemode='a',format='%(asctime)s-%(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


class Command(BaseCommand):
    help = 'Send Exception reports of wrong email joined and incorrect topics by mail'


    def handle(self, *args, **kwargs):
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        path = os.path.join(BASE_DIR, f'Reports/{date.today()}/')

        incorrect_topic_filename = os.path.join(BASE_DIR, f'Reports/{date.today()}/Incorrect_Topics.csv')
        wrong_emails_filename = os.path.join(BASE_DIR, f'Reports/{date.today()}/Wrong_Emails.csv')

        try:
            create_report_path = os.makedirs(os.path.dirname(path), exist_ok=True)

            # get queryset values
            incorrect_topic_queryset = IncorrectTopic.objects.filter(created_on__date=date.today()).values()
            wrong_emails_queryset = StoreOnlineAttendance.objects.filter(created_at__date=date.today()).values('id',
                                                                                                           'uuid',
                                                                                                           'topic_name',
                                                                                                           'section_id',
                                                                                                           'date',
                                                                                                           'wrong_emails',
                                                                                                           'created_at')

            # write a csv for incorrect topics
            with open(incorrect_topic_filename, "wb") as csv_file:
                write_csv(incorrect_topic_queryset, csv_file)

            # write a csv for incorrect topics
            with open(wrong_emails_filename, "wb") as csv_file:
                write_csv(wrong_emails_queryset, csv_file)
            try:
                if not incorrect_topic_queryset and not wrong_emails_queryset:
                    ''' NOTE email while incorrect topics are nothing'''
                    msg = EmailMessage(f'Exception Report {date.today()}',
                                       f'Dear Admin ,\n\
                                                            \nThere is no Incorrect Topics and Wrong emails for  the {date.today()} .\
                                                                \n\nRegards ,\nStudywell Team',
                                       settings.EMAIL_HOST_USER,
                                       ['sumeet@stackfusion.io', 'nadeem.ali@stackfusion.io',
                                        'ravinder.kumar@stackfusion.io',
                                        'rajat.p@lotuspetalfoundation.org'])

                    msg.send(fail_silently=False)

                    logging.info("exception reports mail successfully sent...")



                ''' NOTE : email while incorrect topics and wrong emails are available for today.'''

                # email body
                msg = EmailMessage(f'Exception Report {date.today()}',
                                   f'Dear Admin ,\nPlease find the attached exception reports for Incorrect\
                                        Topics and Wrong emails for student on login for the {date.today()} .\
                                            \n\nRegards ,\nStudywell Team',
                                   settings.EMAIL_HOST_USER,
                                   ['sumeet@stackfusion.io', 'nadeem.ali@stackfusion.io',
                                    'ravinder.kumar@stackfusion.io',
                                    'rajat.p@lotuspetalfoundation.org'])

                msg.attach_file(f'Reports/{date.today()}/Incorrect_Topics.csv')
                msg.attach_file(f'Reports/{date.today()}/Wrong_Emails.csv')
                msg.send(fail_silently=False)

                logging.info("exception reports mail successfully sent...")

            except Exception as e:
                logging.error(f"Error(while send exceptions) : {e}")

        except Exception as e:
            logging.error(f"Error : {e}")
            msg = EmailMessage(f'Error in Exception Report send',
                               f'Dear Admin ,\nPlease find the error in exception reports for Incorrect\
                                                    Topics and Wrong emails for student on login for the {date.today()} .\
                                                        \n\nError : {e}\n\n\nRegards ,\nStudywell Team',
                               settings.EMAIL_HOST_USER,
                               [ 'nadeem.ali@stackfusion.io',]

                                )
            msg.send(fail_silently=False)

