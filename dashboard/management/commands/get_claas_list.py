import os
import sys
import requests
import logging

from django.core.management.base import BaseCommand

from dotenv import load_dotenv

from dashboard.models import Claas, Section, Subject


load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s-%(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')





class Command(BaseCommand):
    help = 'Get list of all the class'

    def get_claas_list(self):

        url = os.getenv('GET_ACADEMICS_DATA_URL')
        header_token = os.getenv('CLASSE365_TOKEN')
        headers = {'Authorization': f'Basic {header_token}'}
        params = {}
        payload = {}

        response = requests.get(
            url, params=params, headers=headers, json=payload
        )

        if response.status_code != 200:
            return { 'status': False, 'message': 'Unable to fetch class details' }

        response_json = response.json()['data']

        return { 'status': True, 'message': response_json }


    def handle(self, *args, **kwargs):

        response_claas = self.get_claas_list()

        # NOTE: IF UNABLE TO FETCH CLASS DETAILS
        if not response_claas['status']:
            logger.error(f"Unable to fetch class details")
            sys.exit()
            

        claas_data = response_claas['message']

        for curr_claas in claas_data:

            claas_name = curr_claas['class_name']
            claas_name_modified = curr_claas['class_name'].lower().split()
            claas_name_modified = ''.join(claas_name_modified)

            # NOTE:     FOR UPDATING CLASS MODEL
            try:
                is_present = Claas.objects.filter(
                    claas_id = curr_claas['class_id']
                ).values()

                if is_present:
                    is_present = is_present[0]
                    if is_present['claas_name'] != claas_name:
                        Claas.objects.filter(
                            id=is_present['id']
                        ).update(
                            claas_name = claas_name,
                            claas_name_for_comparison = claas_name_modified
                        )
                else:
                    Claas.objects.create(
                        claas_id = curr_claas['class_id'], 
                        claas_name = claas_name,
                        claas_name_for_comparison = claas_name_modified
                    )
            except:
                logger.error(f"error while updating class table with class name {claas_name}")
                continue

            # NOTE:     TO UPDATE SECTION MODEL
            sections = curr_claas['section']
            claas_id = curr_claas['class_id']

            for section in sections:
                section_id = section['section_id']
                section_name = section['section_name']
                section_name_modified = section['section_name'].lower().split()
                section_name_modified = ''.join(section_name_modified)

                is_present = Section.objects.filter(
                    section_id=section_id
                ).values()

                if is_present:
                    is_present = is_present[0]

                    if is_present['section_name'] != section_name:
                        Section.objects.filter(
                            id=is_present['id']
                        ).update(
                            section_name = section_name,
                            section_name_for_comparison = section_name_modified
                        )
                else:
                    section_obj = Section(
                        section_id = section_id, 
                        section_name = section_name,
                        section_name_for_comparison = section_name_modified
                    )
                    claas_obj = Claas.objects.get(claas_id=claas_id)
                    section_obj.claas = claas_obj
                    section_obj.save()


                # NOTE:     TO UPDATE SUBJECT MODEL
                subjects = section['subject']
                for subject in subjects:

                    subject_id = subject['subject_id']
                    subject_name = subject['subject_name']
                    subject_name_modified = subject['subject_name'].lower().split()
                    subject_name_modified = ''.join(subject_name_modified)

                    is_present = Subject.objects.filter(
                        subject_id=subject_id
                    ).values()

                    if is_present:
                        is_present = is_present[0]

                        if is_present['subject_id'] != subject_id or \
                                is_present['subject_name'] != subject_name or \
                                is_present['subject_name_for_comparison'] != subject_name_modified :
                            Subject.objects.filter(
                                id=is_present['id']
                            ).update(
                                subject_id = subject_id, 
                                subject_name = subject_name,
                                subject_name_for_comparison = subject_name_modified
                            )
                    else:
                        subject_obj = Subject(
                            subject_id=subject_id, 
                            subject_name=subject_name,
                            subject_name_for_comparison = subject_name_modified
                        )
                        section_obj = Section.objects.get(
                            section_id=section_id
                        )
                        subject_obj.section = section_obj
                        subject_obj.save()

        logger.info('fetching claas data completed !!')


# ===========================================================================================================
#       OLD CODE 
# ===========================================================================================================

        # print(Claas.objects.filter(claas_id=35).values())
        # print(Claas.objects.filter(claas_id=3500).values())
        # is_present[0]['claas_id'] = 3500
        # if is_present[0]['claas_id'] != curr_claas['class_id'] or \
        #                     is_present[0]['claas_name'] != curr_claas['class_name']:
        #     print(Claas.objects.filter(id=is_present[0]['id']).values())
        #                     # .update(claas_id=curr_claas['class_id'], claas_name=curr_claas['class_name'])
        #     print('updated the row')
        # print(Claas.objects.filter(claas_id=35).values())
        # print(Claas.objects.filter(claas_id=3500).values())

        # print('all rows are before deletion')
        # print(Claas.objects.all())
        # print('all rows are deleted')
        # print(Claas.objects.all().values())

        # Claas.objects.all().delete()
        # Section.objects.all().delete()
        # Subject.objects.all().delete()

        # print(Claas.objects.all().values())
        # print(Section.objects.all().values())
        # print(Subject.objects.all().values())



# =======================================================================================================

                    # NOTE: METHOD -- 1
                    # row = Claas(claas_id=curr_claas['class_id'], claas_name=curr_claas['class_name'])
                    # row.save()

                    # NOTE: METHOD -- 2
                    # print(row, created)
                    # row, created = Claas.objects.get_or_create(claas_id=curr_claas['class_id'], claas_name=curr_claas['class_name'])

# ==============================================================================================================
# ==============================================================================================================
