import os
import sys
import requests
import logging

from django.core.management.base import BaseCommand
from dotenv import load_dotenv

from dashboard.models import Teacher, TeacherZoomDetails


load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s-%(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

class Command(BaseCommand):
    help = 'Get All Teachers Zoom Id'


    def get_zoom_users(self):

        url = os.getenv('GET_TEACHERS_ZOOM_ID_URL')
        header_token = os.getenv('ZOOM_API_TOKEN')
        headers = {'Authorization': f'Bearer {header_token}'}
        params = {}
        payload = {}

        response = requests.get(
            url, params=params, headers=headers, json=payload
            )

        if response.status_code != 200:
            return { 'status': False, 'message': 'Unable to fetch zoom users' }

        response_json = response.json()['users']

        return { 'status': True, 'message': response_json }



    def handle(self, *args, **kwargs):

        response_zoom_users = self.get_zoom_users()

        if not response_zoom_users['status']:
            logger.error(f"Unable to fetch teachers zoom id")
            sys.exit()

        zoom_users_data = response_zoom_users['message']

        for curr_teacher in zoom_users_data:
            zoom_id = curr_teacher['id']
            email = curr_teacher['email']

            try:
                teacher_email_obj = Teacher.objects.get(email__icontains=email)
            except:
                logger.error(f"Teacher with the email {email} doesnt exists in our db")
                continue
            try:
                TeacherZoomDetails.objects.get(zoom_id=zoom_id)
            except:
                teacher_zoom_obj = TeacherZoomDetails(zoom_id=zoom_id)
                teacher_email_obj = Teacher.objects.get(email__icontains=email)
                teacher_zoom_obj.teacher = teacher_email_obj
                teacher_zoom_obj.save()

        print('fetching teachers zoom data completed !!')
        logger.info('fetching teachers zoom data completed !!')