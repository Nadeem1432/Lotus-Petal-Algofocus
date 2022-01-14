import json
import logging
from datetime import date
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from attendance.models import StoreOfflineAttendance
from android_app.serializers import (GetAllStudentsOfAClassSerializer,
                                     GetAllTeachersSerializer,
                                     TeacherClassSerializer , SubstitutionTeacherClassSerializer)
from dashboard.models import Section, Student, Teacher
from timetable.models import TimeTable
from datetime import datetime, timedelta
from substitution.models import Substitution
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s-%(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

'''
    NOTE: API to get all the classes to be held today by a teacher.
'''


class GetTeacherClasses(APIView):
    ''' NOTE: Authenticating the user '''
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request_data = request.data

        teacher_classe_365_id = request_data.get('teacher_id')

        ''' NOTE: Verify if teacher_id is valid '''
        teacher_obj = Teacher.objects.filter(classe_365_id=teacher_classe_365_id)

        if not teacher_obj:
            logger.debug(' Invalid teacher_id')
            return Response(
                {
                    "detail": "Invalid teacher_id"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        ''' NOTE: To get the day of the week '''
        day_of_week = TimeTable.find_day_of_week()

        ''' NOTE: Filter all the classes to be held today of a teacher'''




        '''note code for exclude only one period'''
        # get_substituted_classes = Substitution.objects.get(
        #     teacher__classe_365_id=teacher_classe_365_id,
        #     day__day=day_of_week,
        #     substitution_date=date.today()
        # )

        # exclude_date    = get_substituted_classes.substitution_date
        # exclude_period  = get_substituted_classes.period_no.period


        # if get_substituted_classes:
        #     get_classes_from_timetable = TimeTable.objects.filter(
        #         teacher__classe_365_id=teacher_classe_365_id,
        #         day__day=day_of_week,
        #         timetable_date=date.today()
        #
        #     ).exclude(timetable_date=exclude_date , period_no =exclude_period)
        ''' end '''

        get_substituted_classes = Substitution.objects.filter(
            teacher__classe_365_id=teacher_classe_365_id,
            day__day=day_of_week,
            substitution_date=date.today()
        )
        exclude_periods = []

        for period in get_substituted_classes:
            exclude_periods.append(period.period_no.period)


        if get_substituted_classes:
            try:
                get_classes_from_timetable = TimeTable.objects.filter(
                    teacher__classe_365_id=teacher_classe_365_id,
                    day__day=day_of_week,
                    timetable_date=date.today()

                ).exclude( period_no__in =exclude_periods)



                serialized_timetable_data = TeacherClassSerializer(
                    get_classes_from_timetable,
                    many=True
                )

                serialized_substitution_data = SubstitutionTeacherClassSerializer(
                    get_substituted_classes,
                    many=True

                )

                # serialized_data = serialized_substitution_data + serialized_timetable_data
                serialized_data = [serialized_timetable_data.data,serialized_substitution_data.data]
                # serialized_data = serialized_substitution_data.extend(serialized_timetable_data)
                serialized_data = serialized_data
                logger.info('  Got teacher classes  ')

                return Response(serialized_data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"detail":f"{e}"}, status=status.HTTP_200_OK)


        else:
            get_classes = TimeTable.objects.filter(
                teacher__classe_365_id=teacher_classe_365_id,
                day__day=day_of_week,
                timetable_date=date.today()
            )

            serialized_data = TeacherClassSerializer(
                get_classes,
                many=True
            )

            serialized_data = serialized_data.data
            logger.info('  Got teacher classes  ')

            return Response(serialized_data, status=status.HTTP_200_OK)


class GetAllTeachers(APIView):
    ''' NOTE: Authentication the user '''
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    '''
        NOTE: To get the list of all teachers 
    '''

    def get(self, request):
        ''' NOTE: Fetching all teachers stored in our database. '''
        all_teachers_qs = Teacher.objects.all()

        ''' NOTE: Serializing teachers query set '''
        all_teachers_serialized_data = GetAllTeachersSerializer(
            all_teachers_qs,
            many=True
        )

        all_teachers_serialized_data = all_teachers_serialized_data.data
        logger.info(' All Teacher get success.')

        return Response(
            all_teachers_serialized_data,
            status=status.HTTP_200_OK
        )


class GetAllStudentsOfAClass(APIView):
    ''' NOTE: Authenticating the user '''
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        request_data = request.data

        ''' NOTE; Obtaining the section id from the request object'''
        section_id = request_data.get('section_id')

        ''' NOTE: Verifying if the user has passed the section id. '''
        if not section_id:
            logger.error('Section id is not provided')

            return Response(
                {
                    "detail": "Section id is not provided"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        ''' NOTE: Verify if the section id is in the database or not ?'''
        section_id_obj = Section.objects.filter(section_id=section_id)

        if not section_id_obj:
            logger.error('Invalid section_id')
            return Response(
                {
                    "detail": "Invalid section_id"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        ''' NOTE: Fetching all the students of a section through their section id '''
        students_qs = Student.objects.filter(
            section__section_id=section_id
        )

        ''' NOTE: Serializing the student query set obtained above '''
        students_serialized_data = GetAllStudentsOfAClassSerializer(
            students_qs,
            many=True
        )
        students_serialized_data = students_serialized_data.data

        return Response(
            students_serialized_data,
            status=status.HTTP_200_OK
        )


class StoreOfflineAttendanceStatus(APIView):
    ''' NOTE: Authenticating the user '''
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        request_data = request.data

        date = request_data.get('date')
        time_table_id = request_data.get('time_table_id')
        students_attendance_status = request_data.get('attendance_status')

        ''' NOTE: required validation on request parameters (by Nadeem) '''

        if date is None:
            logger.debug(' date required ')
            return Response({"error": {"date": ["This field is required."]}}, status=status.HTTP_400_BAD_REQUEST)

        if time_table_id is None:
            logger.debug(' time_table_id required ')
            return Response({"error": {"time_table_id": ["This field is required."]}},
                            status=status.HTTP_400_BAD_REQUEST)

        if students_attendance_status is None:
            logger.debug(' students_attendance_status required ')
            return Response({"error": {"students_attendance_status": ["This field is required."]}},
                            status=status.HTTP_400_BAD_REQUEST)

        time_table_id = int(time_table_id)
        date = StoreOfflineAttendance.parse_date(date)

        ''' NOTE: Verify time-table id '''
        try:
            time_table_obj = TimeTable.objects.get(
                id=time_table_id
            )
            logger.debug(' time-table id got it ')

        except TimeTable.DoesNotExist:

            logger.error(' Invalid Time-Table id. ')
            return Response(
                {
                    "detail": "Invalid Time-Table id."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            is_attendance_already_stored = StoreOfflineAttendance.objects.get(
                period=time_table_obj,
                date=date
            )

            logger.debug(' The attendance is already stored. ')
            return Response(
                {
                    "detail": "The attendance is already stored."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except StoreOfflineAttendance.DoesNotExist:
            pass

        attendance_list = {}

        for student in students_attendance_status:
            student_id = student.get('id')
            student_status = student.get('status')

            if not student_id or not student_status:
                logger.error("Invalid data passed")

                return Response(
                    {
                        "detail": "Invalid data passed"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            attendance_list[student_id] = {
                "status": student_status,
                "comment": ""
            }

        attendance_list_json = json.dumps(attendance_list)

        try:
            offline_attendance_obj = StoreOfflineAttendance(
                period=time_table_obj,
                date=date,
                attendance_status=attendance_list
            )
            offline_attendance_obj.save()

        except Exception as error:
            logger.error(f"Error :{error}")

            return Response(
                {
                    "detail": "Error saving attendance"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        logger.info("offline attendance successfully saved.")
        return Response(
            {
                "detail": "Successfully saved the attendance."
            },
            status=status.HTTP_200_OK
        )


class GetClassAttendanceAPIView(APIView):
    ''' NOTE: Authenticating the user '''
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        period = self.request.data.get('time_table_id')
        today_date = datetime.now()
        yesterday_date = (today_date - timedelta(days=1)).date()
        yesterday_year = yesterday_date.year
        yesterday_month = yesterday_date.month
        yesterday_day = yesterday_date.day
        year = datetime.now().year
        month = datetime.now().month
        day = datetime.now().day
        today_obj = StoreOfflineAttendance.objects.filter(
            date__year=year,
            date__month=month,
            date__day=day,
            period=period).first()

        yesterday_obj = StoreOfflineAttendance.objects.filter(
            date__year=yesterday_year,
            date__month=yesterday_month,
            date__day=yesterday_day,
            period=period).first()
        today = []
        yesterday = []
        if today_obj is not None:
            items = today_obj.attendance_status.items()
            for key, value in items:
                student = Student.objects.get(student_id=int(key))
                today.append({"sudent_id": key, "name": student.name, "status": value["status"]})

        if yesterday_obj is not None:
            items = yesterday_obj.attendance_status.items()
            for key, value in items:
                student = Student.objects.get(student_id=int(key))
                yesterday.append({"sudent_id": key, "name": student.name, "status": value["status"]})

        return Response({"today": today, "yesterday": yesterday}, status=status.HTTP_200_OK)


class GetOfflineAttendanceAPIView(APIView):

    def post(self, request, *args, **kwargs):
        period = self.request.data.get("time_table_id")
        date = self.request.data.get("date").split("-")
        logger.debug(period)
        logger.debug(date)
        obj = StoreOfflineAttendance.objects.filter(
            date__year=date[0],
            date__month=date[1],
            date__day=date[2],
            period=period).first()
        return_data = []
        if obj is not None:
            items = obj.attendance_status.items()
            for key, value in items:
                student = Student.objects.get(student_id=int(key))
                return_data.append({"sudent_id": key, "name": student.name, "status": value["status"]})

        logger.info("offline attendance got it successfully .")
        return Response(return_data, status=status.HTTP_200_OK)
