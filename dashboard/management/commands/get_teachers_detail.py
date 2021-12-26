import os
import sys
import requests
import logging

from dotenv import load_dotenv
from django.core.management.base import BaseCommand

from dashboard.models import Teacher, Subject


load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s-%(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

class Command(BaseCommand):
    help = 'Get All Teachers Detail'

    def get_teachers_detail(self):

        url = os.getenv('GET_TEACHERS_DATA_URL')
        header_token = os.getenv('CLASSE365_TOKEN')
        headers = {'Authorization': f'Basic {header_token}'}
        params = {"acds_id":"5"}
        payload = {}

        response = requests.get(
            url, params=params, headers=headers, json=payload
        )

        if response.status_code != 200:
            return { 'status': False, 'message': 'Unable to fetch teachers detail'}

        response_json = response.json()['data']

        return { 'status': True, 'message': response_json }


    def handle(self, *args, **kwargs):


        response_teachers = self.get_teachers_detail()

        if not response_teachers['status']:
            logger.error(f"Unable to fetch teachers details")
            sys.exit()


        teachers_data = response_teachers['message']

        for curr_teacher in teachers_data:
            classe_365_id = curr_teacher['id']
            email = curr_teacher['teacher_email']
            first_name = curr_teacher['first_name']
            last_name = curr_teacher['last_name']

            '''TODO : check for only active teachers save into database...'''
            if curr_teacher['checkbox_20'] == os.getenv('INACTIVE_TEACHER_STATUS'):
                continue


            is_present = Teacher.objects.filter(
                classe_365_id=classe_365_id
            ).values()

            if is_present:
                is_present = is_present[0]

                if (is_present['email'] != email or
                        is_present['first_name'] != first_name or
                        is_present['last_name'] != last_name
                    ):
                    Teacher.objects.filter(
                        id = is_present['id']
                    ).update(
                        email=email,
                        first_name=first_name,
                        last_name=last_name
                    )
            else:
                teacher_obj = Teacher(classe_365_id=classe_365_id, email=email, first_name=first_name, last_name=last_name)
                teacher_obj.save()
                subjects = curr_teacher['subjects']
                subjects_obj = []

                for curr_subject in subjects:
                    subject_obj = Subject.objects.get(subject_id=curr_subject['id'])
                    subjects_obj.append(subject_obj)
                teacher_obj.subjects.add(*subjects_obj)

        logger.info('fetching teachers data completed !!')
