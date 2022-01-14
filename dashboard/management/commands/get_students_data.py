import os
import sys
import logging
import requests


from django.core.management.base import BaseCommand

from dotenv import load_dotenv

from dashboard.models import Student, Section


load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s-%(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

class Command(BaseCommand):
    help = 'Get All Teachers Detail'

    def get_students(self):

        url = os.getenv('GET_STUDENTS_DATA_URL')
        header_token = os.getenv('CLASSE365_TOKEN')
        headers = {'Authorization': f'Basic {header_token}'}
        params = { "acds_id": "5" }
        payload = {}

        response = requests.get(
            url, params=params, headers=headers, json=payload
        )

        if response.status_code != 200:
            return { 'status': False, 'message': 'Unable to fetch Students data' }

        response_json = response.json()['data']

        return { 'status': True, 'message': response_json }



    def handle(self, *args, **kwargs):

        response_students = self.get_students()

        if not response_students['status']:
            logger.error(f"Unable to fetch students data")
            sys.exit()

        response_students_data = response_students['message']


        for curr_student in response_students_data:
            student_id = curr_student['id']
            admission_no = curr_student['admission_number']
            email = curr_student['student_email']
            first_name = curr_student['first_name']
            last_name = curr_student['last_name']
            name = f'{first_name} {last_name}'

            '''TODO : check for only active teachers save into database...'''
            if curr_student['text_56'] == os.getenv('DROPOUT_STATUS'):
                continue

            if not student_id or not admission_no or not email or email == 'N/A' or not name or not curr_student['enrollments']:
                logger.error(f"some fields are empty of student with id {student_id}")
                continue

            curr_enrollment_id = 0
            section_id = None

            for enrollment in curr_student['enrollments']:
                if ( enrollment['enrollment_status'] in ['In Progress', 'Upcoming']
                    and 
                    int(enrollment['enrollment_id']) > curr_enrollment_id
                ):
                    curr_enrollment_id = int(enrollment['enrollment_id'])
                    section_id = enrollment['section_id']

                # temp = enrollment['enrollment_date'].split('-')[0]

                # if (temp > curr_enrollment_date) or (temp == curr_enrollment_date and enrollment['enrollment_id'] > curr_enrollment_id):
                #     curr_enrollment_date, curr_enrollment_id = temp, enrollment['enrollment_id']
                #     section_id = enrollment['section_id']


            logger.debug(f'\n\nAdmission no. : {admission_no}. \nSection id : {section_id}')

            ''' NOTE: We ignore if the student is not active '''
            if not section_id:
                logger.debug('The student is inactive, so we are ignoring it')
                continue


            try:
                is_present = Student.objects.get(student_id=student_id)

                if is_present:
                    if (
                        is_present.email != email or
                        is_present.name != name or
                        is_present.section.section_id != section_id
                    ):  
                        section_obj = Section.objects.get(section_id=section_id)
                        Student.objects.filter(
                            id=is_present.id
                        ).update(
                            admission_no=admission_no, 
                            email=email, 
                            name=name,
                            section=section_obj.id
                        )
            except:
                student_obj = Student(student_id=student_id, admission_no=admission_no, email=email, name=name)
                section_obj = Section.objects.get(section_id=section_id)
                student_obj.section = section_obj
                student_obj.save()

        logger.info('fetching students data completed !!')



# ============================================================================================================================
#           OLD CODE
# ============================================================================================================================

            # NOTE: since the api takes almost 2 minutes, so we have entered its data in a file and reading 
            #       from it to save our time
            # with open('/home/app/web/test_data/test.json', 'r') as reader:
            #     # print(reader.read())
            #     data = reader.read()

            # data = json.loads(data)['data']
            # print(data)

# ============================================================================================================================

        # temp1 = Student.objects.get(student_id=1)
        # print(temp1.section.section_id)

# ============================================================================================================================