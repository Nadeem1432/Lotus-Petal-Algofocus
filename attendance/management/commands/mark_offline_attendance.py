import json
import logging
import os
import requests
import sys
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from requests.api import head

from attendance.models import StoreOfflineAttendance


from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s-%(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')



class Command(BaseCommand):
    help = 'Upload attendance from our database to classe-365'


    def get_date_in_string(self, date_time_obj):
    
        date_in_string = date_time_obj.strftime("%Y-%m-%d")

        return date_in_string


    def handle(self, *args, **kwargs):

        curr_time = datetime.now()
        old_time_stamp = curr_time - timedelta(days=1)

        offline_attendance_not_marked_qs = StoreOfflineAttendance.objects.filter(
            date__gte = old_time_stamp,
            is_marked = False, 
        )

        for class_held in offline_attendance_not_marked_qs:

            academic_id = os.getenv('GET_ACADEMIC_ID')
            attendance_url = os.getenv('GET_MANAGE_ATTENDANCE_DATA_URL')
            header_token = os.getenv('CLASSE365_TOKEN')

            headers = {'Authorization': f'Basic {header_token}'}

            claas_id = class_held.period.section.claas.claas_id
            section_id = class_held.period.section.section_id
            subject_id = class_held.period.subject.subject_id
            date = self.get_date_in_string(class_held.date)

            attendance_data = class_held.attendance_status
            attendance_data_json = json.dumps(attendance_data)

            payload = {
                'acds_id': int(academic_id),
                'class_id': int(claas_id),
                'section_id': int(section_id),
                'subject_id': int(subject_id),
                'date': date,
                'working': 1,
                'attendance_data': attendance_data_json
            }

            attendance_response = requests.post(
                attendance_url,
                headers = headers,
                data = payload
            )

            attendance_response_json = attendance_response.json()

            if attendance_response_json['success'] == 1:
                class_held.is_marked = True
                class_held.save()
                logger.info(f'Attendance uploaded. Id : {class_held.id}.')

            else:
                logger.info(f"Error in marking attendance. Id : {class_held.id}.")
