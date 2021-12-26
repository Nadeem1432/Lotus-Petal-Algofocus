import os
import json
import requests
import logging

from django.core.management.base import BaseCommand
from collections import defaultdict
from datetime import time, datetime, timedelta


from dotenv import load_dotenv
# from requests.api import head

from dashboard.models import Claas, Section, Subject, Student, Teacher, TeacherZoomDetails, IsAttendanceMarked


load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s-%(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

class Command(BaseCommand):
    help = 'Get All Teachers Past meetings'

    def get_teacher_meetings(self, teacher_zoom_id):

        get_meetings_url = f'https://api.zoom.us/v2/users/{teacher_zoom_id}/meetings'

        header_token = os.getenv('ZOOM_API_TOKEN')
        headers = {'Authorization': f'Bearer {header_token}'}
        params = {'page_size': 300}
        payload = {}

        response = requests.get(
            get_meetings_url, params=params, headers=headers, json=payload)

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

        # NOTE:     to fetch the details of class, section, subject from the meeting's topic
        topic = topic_name.strip().split('(')

        if len(topic) == 1:
            return {'status': False, 'message': 'The topic name is not valid'}

        subject = topic[0].strip().lower().split()
        subject = ''.join(subject)

        claas = topic[1].split('-')[0].strip().lower().split()
        claas = ''.join(claas)

        # TODO: NAMING BASED ON MULTIPLE SECTIONS AS WELL
        # section = topic[1].split('-')[1].split(')')[0].strip()
        section = topic[1].split('-')

        if len(section) == 1:
            return {'status': False, 'message': 'The topic name is not valid'}

        section = section[1].split(')')[0].strip()
        section = section.split('/')

        sections = []

        for sec in section:
            sec = sec.strip().lower().split()
            sec = ''.join(sec)
            sections.append(sec)

        return {'status': True, 'message': {
            'subject': subject,
            'claas': claas,
            'sections': sections,
        }}



    def find_subject_claas_section_ids(self, subject, claas, sections):

        # NOTE:     while marking attendance we need class id which is stored in a separate table
        try:
            claas_id = Claas.objects.get(claas_name=claas).claas_id
        except:
            return {'status': False, 'message': 'the claas name mentioned is incorrect'}

        # NOTE:     while marking attendance we need section id which is stored in a separate table
        section_ids = []

        for section in sections:
            try:
                section_id = Section.objects.get(
                    section_name=section, claas__claas_name=claas).section_id
                section_ids.append(section_id)
            except:
                return {'status': False, 'message': 'The Section name mentioned is incorrect'}

        # TODO:     MAY BE ISSUE SINCE WE HAVE MULTIPLE SECTION
        # NOTE:     while marking attendance we need subject id which is stored in a separate table
        subject_ids = []

        for section_id in section_ids:
            try:
                subject_id = Subject.objects.get(
                    subject_name=subject, section__section_id=section_id).subject_id
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


        metrics_url = f"https://api.zoom.us/v2/metrics/meetings/{instance_uuid}/participants?type=past"

        header_token = os.getenv('ZOOM_API_TOKEN')
        headers = {'Authorization': f'Bearer {header_token}'}
        params = {}
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



    def generate_attendance_data(self, attendance_data, total_active_time_of_participants):

        min_active_time_for_attendance = os.getenv(
            'GET_MIN_ACTIVE_TIME_FOR_ATTENDANCE')

        # NOTE: CHECK IF THE EMAIL IS PRESENT IN OUR STUDENT DATABASE OR NOT
        for key in total_active_time_of_participants.keys():
            try:
                student_obj = Student.objects.get(email=key)

                is_present = "p" if total_active_time_of_participants[key] >= int(min_active_time_for_attendance) else "a"

                attendance_data[student_obj.student_id] = {
                    "status": is_present, "comment": ""}
            except:
                pass

        return {'status': True, 'message': 'Successfully generated'}



    def generate_current_section_attendance_data(self, attendance_data, section_id):

        curr_section_attendance_data = {}

        # NOTE: FILTER STUDENTS WHO BELONGS TO THIS SECTION ONLY
        for key in attendance_data.keys():
            temp = Student.objects.filter(
                student_id=key, section__section_id=section_id)

            if temp:
                curr_section_attendance_data[key] = attendance_data[key]
            else:
                pass

        # curr_section_attendance_data_json = json.dumps(
        #     curr_section_attendance_data)

        return {'status': True, 'message': curr_section_attendance_data}



    def mark_classe_365_attendance(self, claas_id, section_id, subject_id, date, attendance_data, curr_instance_uuid, curr_meeting_topic):

        attendance_data_json = json.dumps(attendance_data)

        academic_id = os.getenv('GET_ACADEMIC_ID')

        attendance_url = os.getenv('GET_MANAGE_ATTENDANCE_DATA_URL')
        header_token = os.getenv('CLASSE365_TOKEN')
        headers = {'Authorization': f'Basic {header_token}'}

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

        manage_attendance_classe_365_response = requests.post(
            attendance_url, headers=headers, data=payload
        )

        manage_attendance_classe_365_response_json = manage_attendance_classe_365_response.json()

        is_attendance_marked_obj, created = IsAttendanceMarked.objects.get_or_create(
            uuid=curr_instance_uuid
            )

        if manage_attendance_classe_365_response_json['success'] == 1:
            is_attendance_marked_obj.is_marked = True
            print('attendance marked successfully')
            logger.warn(f"Attendance has been marked successfully for the instance with uuid {curr_instance_uuid}")
        else:
            is_attendance_marked_obj.is_marked = False
            print('error in marking attendance')
            logger.error(f"Unable to mark attendance of the instance with uuid {curr_instance_uuid} in classe 365")

        is_attendance_marked_obj.save()


    def append_headers_to_file(self):
        
        filename = f"/home/app/web/data/unable_to_fetch_meeting.txt"
        with open(filename, "a") as file:
            file.write("first name, last name, email")

        
        filename = f"/home/app/web/data/incorrect_topic.txt"
        with open(filename, "a") as file:
            file.write("email, start time, meeting id(unique), topic")


        filename = f"/home/app/web/data/incorrect_section_class_subject.txt"
        with open(filename, "a") as file:
            file.write("email, start time, meeting id(unique), topic")




    def handle(self, *args, **kwargs):

        self.append_headers_to_file()

        all_teachers = TeacherZoomDetails.objects.all()

        # NOTE: WE ITERATE OVER ALL TEACHERS AND GET IT'S MEETINGS AND MARK THE ATTENDANCE
        for teacher in all_teachers:

            response_meetings = self.get_teacher_meetings(teacher.zoom_id)

            # NOTE: IF UNABLE TO FETCH MEETINGS, WE CONITNUE FOR NEXT TEACHER
            if not response_meetings['status']:

                filename = f"/home/app/web/data/unable_to_fetch_meeting.txt"
                with open(filename, "a") as file:
                    file.write("\n")
                    # first name, last name, email
                    file.write(teacher.teacher.first_name + ", ")
                    file.write(teacher.teacher.last_name + ", ")
                    file.write(teacher.teacher.email)

                logger.error(f" (Testing) Unable to fetch the teacher meeting with id {teacher.zoom_id}")
                continue

            # NOTE: IF WE GET A VALID RESPONSE
            meetings = response_meetings['message']


            for curr_meeting in meetings:

                meeting_topics = curr_meeting['topic'].split('+')

                for curr_meeting_topic in meeting_topics:

                    response_topic = self.get_subject_class_section_from_topic(
                        curr_meeting_topic)

                    # NOTE: IF THE TOPIC NAME FORMAT IS INCORRECT
                    if not response_topic['status']:

                        filename = f"/home/app/web/data/incorrect_topic.txt"
                        with open(filename, "a") as file:
                            file.write("\n")
                            # email, start time, meeting id(unique), topic
                            file.write(teacher.teacher.email + " , ")

                            try:
                                time = curr_meeting['start_time'][:10]
                                file.write(time + " , ")
                            except:
                                file.write(" , ")

                            file.write( str(curr_meeting['id']) + " , ")
                            file.write(curr_meeting['topic'])

                        logger.error(f" (Testing) The topic name is incorrect of meeting with id {curr_meeting['id']}. Topic : {curr_meeting_topic}")
                        continue


                    response_topic_message = response_topic['message']
                    subject = response_topic_message['subject']
                    claas = response_topic_message['claas']
                    sections = response_topic_message['sections']


                    response_subject_claas_section_ids = self.find_subject_claas_section_ids(
                        subject, claas, sections)


                    # NOTE: IF THE SUBJECT, CLAAS, OR SECTION IS EITHER INCORRECT OR NOT PRESENT IN OUR DB
                    if not response_subject_claas_section_ids['status']:
                        
                        filename = f"/home/app/web/data/incorrect_section_class_subject.txt"
                        with open(filename, "a") as file:
                            file.write("\n")
                            # email, start time, meeting id(unique), topic
                            file.write(teacher.teacher.email + " , ")

                            try:
                                time = curr_meeting['start_time'][:10]
                                file.write(time + " , ")
                            except:
                                file.write(" , ")

                            file.write( str(curr_meeting['id']) + " , ")
                            file.write(curr_meeting['topic'])

                        logger.error(f"(Testing) Either the subject, class or section is incorrect or not in our db of the meeting with id {curr_meeting['id']}. Topic: {curr_meeting_topic}")
                        continue


                    response_subject_claas_section_ids_message = response_subject_claas_section_ids[
                        'message']

                    claas_id = response_subject_claas_section_ids_message['claas_id']
                    section_ids = response_subject_claas_section_ids_message['section_ids']
                    subject_ids = response_subject_claas_section_ids_message['subject_ids']

                    response_meeting_instances = self.get_meeting_instances(
                        curr_meeting['id'])

                    # NOTE: IF THERE IS ERROR WHILE FETCHING MEETING INSTANCES
                    if not response_meeting_instances['status']:
                        logger.error(f"(Testing) Unable to fetch meeting instance of meeting with id {curr_meeting['id']}")
                        continue


                    curr_meeting_instances = response_meeting_instances['message']


                    for curr_instance in curr_meeting_instances:

                        # TODO: MAKE IT IN SEPARATE FUNCTION
                        # NOTE: IGNORE MEETINGS CONDUCTED BEFORE 29th OF JUNE
                        curr_instance_date = curr_instance['start_time'].split('T')[0]

                        # TODO:
                        # print(curr_instance_date)

                        if curr_instance_date < '2021-08-01':
                            logger.warn(f"(Testing) Since the meeting is of before August the attendance wont be marked of instance with uuid {curr_instance['uuid']}. (Testing)")
                            continue


                        curr_instance_uuid = curr_instance['uuid']

                        # NOTE: IGNORE MEETINGS WHOSE ATTENDANCE IS ALREADY MARKED
                        # try:
                        #     is_attendance_marked = IsAttendanceMarked.objects.get(
                        #         uuid=curr_instance_uuid)

                        #     if is_attendance_marked.is_marked:
                        #         logger.warn(f"the attendance is already marked for the instance with uuid {curr_instance['uuid']}")
                        #         continue
                        # except:
                        #     pass



                        response_instance_metrics = self.get_instance_metrics(
                            curr_instance_uuid)


                        # NOTE: IF THERE IS ERROR WHILE FETCHING METRICS
                        if not response_instance_metrics['status']:
                            logger.error(f" (Testing) Unable to fetch metrics data of the instance with uuid {curr_instance['uuid']}. \
                                            Topic : {curr_meeting_topic}. \
                                            Start time : {curr_instance['start_time']} ")
                            continue


                        curr_instance_metrics = response_instance_metrics['message']

                        total_active_time_of_participants = defaultdict(int)

                        for curr_participant in curr_instance_metrics:

                            # active_time = self.get_active_time_of_participant(
                            #     curr_participant)

                            # NOTE:  CHECKING WHETHER THE PARTICIPANT HAS JOINED WITH EMAIL OR NOT
                            #           IF IT DOESN'T WE IGNORE IT
                            try:
                                email = curr_participant['email']

                                # filename = f"/Users/hemant/Documents/stackfusion/lotuspetal/lotuspetal-backend/emails/{claas}.txt"
                                filename = f"/home/app/web/data/emails/{claas}.txt"
                                with open(filename, "a") as file:
                                    file.write("\n")
                                    # start time, class, subject, user name, email
                                    file.write( curr_instance['start_time'][:10] + " , ")
                                    file.write( claas + " , ")
                                    file.write( subject + " , ")
                                    file.write( curr_participant['user_name'] + " , ")
                                    file.write( email )
                                    file.write("\n")

                            except:
                                filename = f"/home/app/web/data/noemails/{claas}.txt"
                                with open(filename, "a") as file:
                                    file.write("\n")
                                    # start time, class, subject, user name
                                    file.write( curr_instance['start_time'][:10] + " , " )
                                    file.write( claas + " , " )
                                    file.write( subject + " , " )
                                    file.write( curr_participant['user_name'] )
                                    file.write("\n")
                        


                            # total_active_time_of_participants[email] += active_time

                        # TODO:
                        # print(total_active_time_of_participants)



                        # attendance_data = {}

                        # self.generate_attendance_data(
                        #     attendance_data, total_active_time_of_participants)

                        # # NOTE: iterating on all section whose class has been conducted together
                        # #       bcos we have to mark the attendance separately
                        # for i in range(len(section_ids)):
                        #     section_id = section_ids[i]
                        #     subject_id = subject_ids[i]

                        #     response_generate_current_section_attendance_data = self.generate_current_section_attendance_data(
                        #         attendance_data, section_id)

                        #     curr_section_attendance_data = response_generate_current_section_attendance_data[
                        #         'message']


                        #     if not curr_section_attendance_data:
                        #         is_attendance_marked_obj, created = IsAttendanceMarked.objects.get_or_create(
                        #             uuid=curr_instance_uuid
                        #         )

                        #         is_attendance_marked_obj.is_marked = True
                        #         is_attendance_marked_obj.save()
                        #         logger.error(f"Since there are no participants logged in with the required domain the attendance wont be marked for the instance with uuid {curr_instance['uuid']}")
                        #         continue


                        #     self.mark_classe_365_attendance(claas_id, section_id, subject_id, curr_instance_date,
                        #                                     curr_section_attendance_data, curr_instance_uuid, curr_meeting_topic)



