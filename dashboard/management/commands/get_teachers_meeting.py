import json
import logging
import os
import re
import requests

from django.core.management.base import BaseCommand
from collections import defaultdict
from datetime import time, datetime, timedelta, date


from dotenv import load_dotenv

from dashboard.models import (
    Claas, 
    IncorrectTopic,
    # IsAttendanceMarked,
    Section, 
    Student,
    Subject, 
    Teacher, 
    TeacherZoomDetails, 
    IncorrectTopic,
    # WrongEmail,
    ClaasAlias,
)
from dashboard.utils import fetch_date_time
from attendance.models import StoreOnlineAttendance



load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s-%(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

class Command(BaseCommand):
    help = 'Get All Teachers Past meetings'

    def get_teacher_meetings(self, teacher_zoom_id):

        get_meetings_url = f'https://api.zoom.us/v2/users/{teacher_zoom_id}/meetings'

        header_token = os.getenv('ZOOM_API_TOKEN')
        headers = {'Authorization': f'Bearer {header_token}'}
        params = {'page_size': 300}
        payload = {}

        response = requests.get(
            get_meetings_url, params=params, headers=headers, json=payload
        )

        # NOTE: IF WE DON'T GET A VALID RESPONSE WE RETURN
        if response.status_code != 200:
            return {'status': False, 'message': 'unable to fetch meeting details'}

        response_json = response.json()

        # NOTE: WE WILL CHECK IF THERE ARE MORE MEETINGS WHICH WE CAN GET BY next_page_token
        meetings = response_json['meetings']

        while response_json['next_page_token']:
            params['next_page_token'] = response_json['next_page_token']

            response = requests.get(
                get_meetings_url, params=params, headers=headers, json=payload
            )

            response_json = response.json()
            meetings.extend(response_json['meetings'])

        return {'status': True, 'message': meetings}



    def get_subject_class_section_from_topic(self, topic_name):

        ''' NOTE: to fetch the details of class, section, subject from the meeting's topic '''

        splitted_topic = topic_name.split('/')

        if len(splitted_topic) < 3 :
            return {'status': False, 'message': 'The topic name is not valid'}

        subject = splitted_topic[0].strip().lower().split()
        subject = ''.join(subject)

        claas = splitted_topic[1].strip().lower().split()
        claas = ''.join(claas)

        try:
            claas_alias_qs = ClaasAlias.objects.get(name__iexact = claas)
            claas = claas_alias_qs.claas.claas_name_for_comparison
        except ClaasAlias.MultipleObjectsReturned:
            return {
                'status': False,
                'message' : 'Multiple Objects returned'
            }
        except ClaasAlias.DoesNotExist:
            return {
                'status': False,
                'message': 'The Class Alias is not present in our database'
            }

        sections = []
        for i in range(2, len(splitted_topic)):
            section = splitted_topic[i].strip().lower().split()
            section = ''.join(section)

            sections.append("section" + section)

        return {
            'status': True, 
            'message': {
                'claas': claas,
                'subject': subject,
                'sections': sections,
        }}



    def find_subject_claas_section_ids(self, subject, claas, sections):

        # NOTE:     while marking attendance we need class id which is stored in a separate table
        try:
            claas_id = Claas.objects.get(
                claas_name_for_comparison = claas
            ).claas_id
        except:
            return {'status': False, 'message': 'the claas name mentioned is incorrect'}

        # NOTE:     while marking attendance we need section id which is stored in a separate table
        section_ids = []

        for section in sections:
            try:
                section_id = Section.objects.get(
                    section_name_for_comparison = section, 
                    claas__claas_name_for_comparison = claas
                ).section_id
                section_ids.append(section_id)
            except:
                return {'status': False, 'message': 'The Section name mentioned is incorrect'}

        # TODO:     MAY BE ISSUE SINCE WE HAVE MULTIPLE SECTION
        # NOTE:     while marking attendance we need subject id which is stored in a separate table
        subject_ids = []

        for section_id in section_ids:
            try:
                subject_id = Subject.objects.get(
                    subject_name_for_comparison = subject, 
                    section__section_id = section_id
                ).subject_id
                subject_ids.append(subject_id)
            except:
                return {'status': False, 'message': 'The Subject name mentioned is incorrect'}

        return {'status': True, 'message': {
            'claas_id': claas_id,
            'section_ids': section_ids,
            'subject_ids': subject_ids,
        }}



    def get_meeting_instances(self, meeting_id):

        instances_url = f"https://api.zoom.us/v2/past_meetings/{meeting_id}/instances"

        header_token = os.getenv('ZOOM_API_TOKEN')
        headers = {'Authorization': f'Bearer {header_token}'}
        params = {}
        payload = {}

        instances_response = requests.get(
            instances_url, params=params, headers=headers, json=payload
        )

        # NOTE: IF WE DON'T GET VALID RESPONSE WE RETURN
        if instances_response.status_code != 200:
            return {'status': False, 'message': 'Unable to fetch the instances'}

        instances_response_json = instances_response.json()['meetings']

        # NOTE: IF THE RESPONSE IS VALID, WE WILL RETURN THE INSTANCES
        return {'status': True, 'message': instances_response_json}



    def get_instance_metrics(self, instance_uuid):

        # TODO: ALSO CHECK FOR NEXT PAGE TOKEN AND ADD THOSE
        metrics_url = f"https://api.zoom.us/v2/metrics/meetings/{instance_uuid}/participants?type=past"

        header_token = os.getenv('ZOOM_API_TOKEN')
        headers = {'Authorization': f'Bearer {header_token}'}
        params = { 'page_size': 300 }
        payload = {}

        metrics_response = requests.get(
            metrics_url, params=params, headers=headers, json=payload
        )

        # NOTE: IF WE DON'T GET VALID RESPONSE WE RETURN
        if metrics_response.status_code != 200:
            return {'status': False, 'message': 'Unable to fetch the metrics of the instance'}

        metrics_response_json = metrics_response.json()['participants']

        # NOTE: IF THE RESPONSE IS VALID WE WILL RETURN THE PARTICIPANTS
        return {'status': True, 'message': metrics_response_json}



    def get_active_time_of_participant(self, curr_participant):

        join_time = curr_participant['join_time'].split('T')[1]
        joined_at = time(int(join_time[:2]), int(
            join_time[3:5]), int(join_time[6:8]))
        joined_delta = timedelta(
            hours=joined_at.hour, minutes=joined_at.minute, seconds=joined_at.second)

        leave_time = curr_participant['leave_time'].split('T')[1]
        leaved_at = time(int(leave_time[:2]), int(
            leave_time[3:5]), int(leave_time[6:8]))
        leaved_delta = timedelta(
            hours=leaved_at.hour, minutes=leaved_at.minute, seconds=leaved_at.second)

        active_time = leaved_delta - joined_delta
        active_time = (active_time.seconds // 60) % 60

        return active_time



    # def generate_attendance_data(self, attendance_data, total_active_time_of_participants):

    #     min_active_time_for_attendance = os.getenv('GET_MIN_ACTIVE_TIME_FOR_ATTENDANCE')

    #     # NOTE: CHECK IF THE EMAIL IS PRESENT IN OUR STUDENT DATABASE OR NOT
    #     for key in total_active_time_of_participants.keys():
    #         try:
    #             student_obj = Student.objects.get(email=key)

    #             is_present = "p" if total_active_time_of_participants[key] >= int(min_active_time_for_attendance) else "a"

    #             attendance_data[student_obj.student_id] = {"status": is_present, "comment": ""}
    #         except:
    #             pass

    #     return {'status': True, 'message': 'Successfully generated'}



    def generate_current_section_attendance_data(self, total_active_time_of_participants, section_id):

        min_active_time_for_attendance = os.getenv('GET_MIN_ACTIVE_TIME_FOR_ATTENDANCE')
        curr_section_attendance_data = {}

        students = Student.objects.filter(section__section_id = section_id)

        for student in students:
            student_is_present = total_active_time_of_participants.get(student.email)

            is_meeting_criteria = "a"
            if student_is_present and total_active_time_of_participants[student.email] >= int(min_active_time_for_attendance):
                is_meeting_criteria = "p"
            
            curr_section_attendance_data[student.student_id] = { "status": is_meeting_criteria, "comment": "" }

        

        # # NOTE: FILTER STUDENTS WHO BELONGS TO THIS SECTION ONLY
        # for key in attendance_data.keys():
        #     temp = Student.objects.filter(
        #                 student_id=key, 
        #                 section__section_id=section_id
        #             )

        #     if temp:
        #         curr_section_attendance_data[key] = attendance_data[key]
        #     else:
        #         pass

        # curr_section_attendance_data_json = json.dumps(
        #     curr_section_attendance_data)

        return {'status': True, 'message': curr_section_attendance_data}


    def get_date_in_string(self, date_time_obj):
        
        date_in_string = date_time_obj.strftime("%Y-%m-%d")

        return date_in_string


    def mark_classe_365_attendance(
            self,
            claas_id,
            section_id,
            subject_id,
            meeting_time,
            attendance_data,
            curr_instance_uuid,
            meeting_topic,
            curr_meeting_id,
            wrong_emails,
            curr_teacher_email,
        ):

        attendance_data_json = json.dumps(attendance_data)

        # print(attendance_data_json)
        # return

        academic_id = os.getenv('GET_ACADEMIC_ID')

        attendance_url = os.getenv('GET_MANAGE_ATTENDANCE_DATA_URL')
        header_token = os.getenv('CLASSE365_TOKEN')
        headers = {'Authorization': f'Basic {header_token}'}

        date = self.get_date_in_string(meeting_time)

        payload = {
            'acds_id': int(academic_id),
            'class_id': int(claas_id),
            'section_id': int(section_id),
            'subject_id': int(subject_id),
            'date': date,
            'working': 1,
            'attendance_data': attendance_data_json
        }
        print()
        print(payload)


        # TODO: TEMPORARY
        # return


        manage_attendance_classe_365_response = requests.post(
            attendance_url, headers=headers, data=payload
        )

        manage_attendance_classe_365_response_json = manage_attendance_classe_365_response.json()

                                            
        try:
            is_attendance_marked_obj = StoreOnlineAttendance.objects.get(
                uuid = curr_instance_uuid
            )
        except StoreOnlineAttendance.DoesNotExist:
            section_obj = Section.objects.get(section_id = section_id)

            is_attendance_marked_obj = StoreOnlineAttendance(
                uuid = curr_instance_uuid,
                topic_name = meeting_topic,
                section = section_obj,
                date = meeting_time,
                attendance_status = json.loads(attendance_data_json),
                wrong_emails = wrong_emails,
            )


        if manage_attendance_classe_365_response_json['success'] == 1:
            is_attendance_marked_obj.is_marked = True
            is_attendance_marked_obj.save()
            print('attendance marked successfully')
            logger.error('attendance marked successfully')

            # logger.error(f"Attendance has been marked successfully for the instance with uuid {curr_instance_uuid}")
        else:
            is_attendance_marked_obj.is_marked = False
            is_attendance_marked_obj.save()

            print('error in marking attendance')
            logger.error(f"Unable to mark attendance of the instance with uuid {curr_instance_uuid} in classe 365")
            logger.error(
                        str( datetime.now().date() )
                        + 
                        f" : Topic - {meeting_topic}. "
                        +
                        f"The topic is incorrect of meeting with id : {curr_meeting_id}. "
                        + 
                        f"The teacher's email is : {curr_teacher_email}"

            )




    def handle(self, *args, **kwargs):

        all_teachers = TeacherZoomDetails.objects.all()

        ''' NOTE: WE ITERATE OVER ALL TEACHERS AND GET IT'S MEETINGS AND MARK THE ATTENDANCE '''
        for teacher in all_teachers:

            print('\n\n\nBEGIN :- \nteacher zoom id' + str(teacher.zoom_id))

            response_meetings = self.get_teacher_meetings(teacher.zoom_id)

            # NOTE: IF UNABLE TO FETCH MEETINGS, WE CONITNUE FOR NEXT TEACHER
            if not response_meetings['status']:
                logger.error(
                    str(datetime.now().date())
                    +
                    f" : Unable to fetch the teacher meeting with id {teacher.zoom_id}. "
                    + 
                    f"Teacher's email is : {teacher.teacher.email}."
                )
                continue

            # NOTE: IF WE GET A VALID RESPONSE
            meetings = response_meetings['message']


            for curr_meeting in meetings:

                print('topic' + curr_meeting['topic'])
                print('meeting id' + str(curr_meeting['id']))

                meeting_topic_splitted = curr_meeting['topic'].split('+')

                for meeting_topic in meeting_topic_splitted:

                    ''' NOTE: IF MEETING ID IS ALREADY PRESENT IN INCORRECT TOPIC TABLE IGNORE IT '''
                    is_present = IncorrectTopic.objects.filter(meeting_id = curr_meeting['id'])

                    if is_present:
                        logger.debug("The meeting's topic name is incorrect and already added in the incorrect topic table.")
                        continue

                    response_topic = self.get_subject_class_section_from_topic(
                        meeting_topic
                    )


                    # TODO: SEND EMAIL TO LOTUS PETAL TEAM
                    # NOTE: IF THE TOPIC NAME FORMAT IS INCORRECT
                    if not response_topic['status']:
                        teacher_name = teacher.teacher.first_name + teacher.teacher.last_name
                        meeting_start_time_str = curr_meeting.get('start_time')

                        incorrect_topic_obj = IncorrectTopic(
                                                topic = meeting_topic,
                                                meeting_id = curr_meeting['id'],
                                                teacher_name = teacher_name,
                                            )
                        if meeting_start_time_str:
                            meeting_start_time = fetch_date_time(meeting_start_time_str)
                            incorrect_topic_obj.meeting_time = meeting_start_time
                            
                        incorrect_topic_obj.save()
                        
                        logger.error(
                            str( datetime.now().date() )
                            + 
                            f" : Topic - {meeting_topic}. "
                            +
                            f"The topic is incorrect of meeting with id : {curr_meeting['id']}. "
                            + 
                            f"The teacher's email is : {teacher.teacher.email}"
                        )
                        continue


                    response_topic_message = response_topic['message']
                    subject = response_topic_message['subject']
                    claas = response_topic_message['claas']
                    sections = response_topic_message['sections']

                    response_subject_claas_section_ids = self.find_subject_claas_section_ids(
                        subject, 
                        claas, 
                        sections
                    )


                    # TODO: SEND EMAIL TO THE LOTUS PETAL TEAM
                    # NOTE: IF EITHER SUBJECT, CLAAS, OR SECTION IS INCORRECT OR NOT PRESENT IN OUR DB
                    if not response_subject_claas_section_ids['status']:
                        teacher_name = teacher.teacher.first_name + teacher.teacher.last_name
                        meeting_start_time_str = curr_meeting.get('start_time')

                        incorrect_topic_obj = IncorrectTopic(
                                                topic = meeting_topic,
                                                meeting_id = curr_meeting['id'],
                                                teacher_name = teacher_name
                                            )
                        if meeting_start_time_str:
                            meeting_start_time = fetch_date_time(meeting_start_time_str)
                            incorrect_topic_obj.meeting_time = meeting_start_time

                        incorrect_topic_obj.save()

                        logger.error(
                            str(datetime.now().date())
                            + 
                            f" : Topic - {meeting_topic}. "
                            +
                            f"Either the subject - {subject}, class - {claas}, or sections - {sections} is incorrect"
                            +
                            f" or not in our database of the meeting with id {curr_meeting['id']}. "
                            +
                            f"The teacher's email is : {teacher.teacher.email}."
                        )
                        continue

                    response_subject_claas_section_ids_message = response_subject_claas_section_ids['message']

                    claas_id = response_subject_claas_section_ids_message['claas_id']
                    section_ids = response_subject_claas_section_ids_message['section_ids']
                    subject_ids = response_subject_claas_section_ids_message['subject_ids']


                    response_meeting_instances = self.get_meeting_instances(curr_meeting['id'])

                    # NOTE: IF THERE IS ERROR WHILE FETCHING MEETING INSTANCES
                    if not response_meeting_instances['status']:
                        logger.error(
                            str(datetime.now().date())
                            + 
                            f" : Unable to fetch meeting instance of meeting with id {curr_meeting['id']}. "
                            + 
                            f"The teacher's email is : {teacher.teacher.email}."
                        )
                        continue

                    curr_meeting_instances = response_meeting_instances['message']

                    for curr_instance in curr_meeting_instances:

                        # TODO: FROM .ENV FILE and in native time obj
                        meetings_before_date_to_ignore = '2021-09-13'

                        # TODO: MAKE IT IN SEPARATE FUNCTION
                        # NOTE: IGNORE MEETINGS CONDUCTED BEFORE AUGUST
                        curr_instance_date = curr_instance['start_time'].split('T')[0]

                        curr_instance_meeting_time = fetch_date_time(curr_instance['start_time'])

                        # TODO: Make this comparision through datetime function not string
                        if curr_instance_date < meetings_before_date_to_ignore:
                            print(
                                str(datetime.now().date())
                                +
                                f" : Since the meeting is of before {meetings_before_date_to_ignore} "
                                +
                                f"the attendance wont be marked. The instance uuid is {curr_instance['uuid']}"
                            )
                            logger.error(
                                str(datetime.now().date())
                                +
                                f" : Since the meeting is of before {meetings_before_date_to_ignore} "
                                +
                                f"the attendance wont be marked. The instance uuid is {curr_instance['uuid']}"
                            )
                            continue

                        ''' NOTE: Ignore future meetings '''
                        curr_time = datetime.now()
                        if curr_instance_meeting_time > curr_time:
                            print(
                                str(datetime.now().date())
                                + 
                                f" : Since the meeting is of future timestamp :{curr_time} "
                                +
                                f"the attendance won't be marked. The instance uuid is {curr_instance['uuid']}"
                            )
                            continue

                        # NOTE: IGNORE MEETINGS WHOSE ATTENDANCE IS ALREADY MARKED
                        curr_instance_uuid = curr_instance['uuid']

                        try:
                            is_attendance_marked = StoreOnlineAttendance.objects.get(
                                uuid = curr_instance_uuid
                            )

                            if is_attendance_marked.is_marked:
                                print(
                                    str(datetime.now().date())
                                    +    
                                    f"the attendance is already marked for the instance with uuid {curr_instance['uuid']}"
                                )
                                continue
                        except:
                            pass

                        response_instance_metrics = self.get_instance_metrics(
                            curr_instance_uuid
                        )

                        # NOTE: IF THERE IS ERROR WHILE FETCHING METRICS
                        if not response_instance_metrics['status']:
                            logger.error(f"Unable to fetch metrics data of the instance with uuid {curr_instance['uuid']}")
                            continue

                        curr_instance_metrics = response_instance_metrics['message']


                        total_active_time_of_participants = defaultdict(int)
                        wrong_emails = {}

                        for curr_participant in curr_instance_metrics:

                            # NOTE:  CHECKING WHETHER THE PARTICIPANT HAS JOINED WITH EMAIL OR NOT
                            email = curr_participant.get('email')
                            user_name = curr_participant.get('user_name')

                            if not email:                                
                                wrong_emails[user_name] = ''
                                continue
                            
                            ''' NOTE: We check whether the domain is of lotuspetal ? '''
                            regex = r'^[A-Za-z0-9._%+-]+@lotuspetalfoundation.org$'
                            is_lotuspetal_domain = re.fullmatch(regex, email)

                            if not is_lotuspetal_domain:
                                wrong_emails[user_name] = email
                                continue
                            
                            # TODO:
                            active_time = self.get_active_time_of_participant(
                                curr_participant
                            )

                            total_active_time_of_participants[email] += active_time

                        # attendance_data = {}

                        # self.generate_attendance_data(
                        #         attendance_data, 
                        #         total_active_time_of_participants
                        # )

                        # NOTE: iterating on all section whose class has been conducted together
                        #       bcos we have to mark the attendance separately
                        for i in range(len(section_ids)):
                            section_id = section_ids[i]
                            subject_id = subject_ids[i]
                            
                            # TODO: MIN ACTIVE TIME ?
                            response_generate_current_section_attendance_data = self.\
                                generate_current_section_attendance_data(
                                    # attendance_data, 
                                    total_active_time_of_participants,
                                    section_id
                                )

                            curr_section_attendance_data = response_generate_current_section_attendance_data['message']

                            if not curr_section_attendance_data:
                                is_attendance_marked_obj_present = StoreOnlineAttendance.objects.filter(
                                    uuid = curr_instance_uuid
                                )

                                if not is_attendance_marked_obj_present:
                                    section_obj = Section.objects.get(section_id=section_id)

                                    is_attendance_marked_obj = StoreOnlineAttendance(
                                        uuid = curr_instance_uuid,
                                        topic_name = meeting_topic,
                                        section = section_obj,
                                        # period 
                                        date = curr_instance_meeting_time,
                                        attendance_status = json.dumps(curr_section_attendance_data),
                                        wrong_emails = wrong_emails,
                                        is_marked = False,
                                    )
                                    is_attendance_marked_obj.save()
                                
                                logger.error(f"the attendance json didn't have any object of the instance with uuid {curr_instance['uuid']}")
                                continue
                            
                            print('correct topic')
                            logger.debug('correct topic')
                            print('zoom id' + str(teacher.zoom_id))
                            logger.debug('zoom id' + str(teacher.zoom_id))
                            print('topic' + curr_meeting['topic']+'\n')
                            logger.debug('topic' + curr_meeting['topic']+'\n')

                            self.mark_classe_365_attendance(
                                claas_id,
                                section_id,
                                subject_id,
                                curr_instance_meeting_time,
                                curr_section_attendance_data, 
                                curr_instance_uuid, 
                                meeting_topic,
                                curr_meeting['id'],
                                wrong_emails,
                                teacher.teacher.email
                            )

            print('\n\n END :- ')
            logger.info('\n\n END :- ')

        print('TASK - MARK ATTENDANCE IS COMPLETE !!')
        logger.info('TASK - MARK ATTENDANCE IS COMPLETE !!')