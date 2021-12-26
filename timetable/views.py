from django.core.exceptions import ValidationError
import requests
import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from dashboard.models import Claas, Section, Subject, Teacher
from timetable.models import TimeTable, Day, Period
from timetable.serializers import (AllClaasSectionSerializer,
                                   AllSubjectTeacherSerializer,
                                   TimeTableSerializer)
from datetime import datetime

# logger config
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s-%(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')




class AllClassSection(APIView):

    ''' NOTE: Authenticating the user '''
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):

        all_claas_qs = Claas.objects.all()

        all_claas_serialized_data = AllClaasSectionSerializer(
            all_claas_qs,
            many = True
        )

        all_claas_serialized_data = all_claas_serialized_data.data

        return Response(
            all_claas_serialized_data,
            status = status.HTTP_200_OK
        )


class AllTeacherSubject(APIView):

    ''' NOTE: Authenticating the user '''
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        request_data = request.data

        section_id = request_data.get('section_id')

        ''' NOTE: Check if section id is sent ? '''
        if not section_id:
            return Response(
                {
                    "detail": "Invalid parameters. Section id is not sent"
                },
                status = status.HTTP_400_BAD_REQUEST
            )

        ''' NOTE: Check if the section id is valid or not'''
        section_obj = Section.objects.filter(section_id = section_id)

        if not section_obj:
            return Response(
                {
                    "detail": "Invalid parameters. Section id is invalid"
                },
                status = status.HTTP_400_BAD_REQUEST
            )

        subject_of_section_qs = Subject.objects.filter(
            section__section_id = section_id
        )

        all_subjects_serialized = AllSubjectTeacherSerializer(
            subject_of_section_qs,
            many = True
        )

        all_subjects_serialized_data = all_subjects_serialized.data

        return Response(
            all_subjects_serialized_data,
            status = status.HTTP_200_OK
        )


class GetTimeTable(APIView):

    ''' NOTE: Authenticating the user '''
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        request_data = request.data

        section_id = request_data.get('section_id')
        week = request_data.get('week')
        month = request_data.get('month')
        year = request_data.get('year')

        ''' NOTE: Check if section id is sent ? '''
        if not section_id:
            return Response(
                {
                    "detail": "Invalid parameters. Section id is not sent"
                },
                status = status.HTTP_400_BAD_REQUEST
            )

        ''' NOTE: Check if the section id is valid or not'''
        section_obj = Section.objects.filter(section_id = section_id,
                                             # timetable_week = week,
                                             # timetable_month = month,
                                             # timetable_year = year
                                             )

        if not section_obj:
            return Response(
                {
                    "detail": "Invalid parameters. Section id is invalid"
                },
                status = status.HTTP_400_BAD_REQUEST
            )

        timetable_qs = TimeTable.objects.filter(
                section__section_id = section_id,
                timetable_week = week,
                 timetable_month = month,
                 timetable_year = year

        )

        timetable_serialized = TimeTableSerializer(
            timetable_qs,
            many = True
        )

        timetable_serialized_data = timetable_serialized.data

        return Response(
            timetable_serialized_data,
            status = status.HTTP_200_OK
        )


class UpdateTimeTable(APIView):

    ''' NOTE: Authenticating the user '''
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        request_data = request.data
        logger.debug(f'request data - \n{request_data}')

        section_id = request_data[0].get('section_id')
        days = request_data[1].get('days')

        ''' NOTE: Check if section id is sent ? '''
        if not section_id:
            return Response(
                {
                    "detail": "Invalid parameters. Section id is not sent"
                },
                status = status.HTTP_400_BAD_REQUEST
            )

        ''' NOTE: Check if time table data is sent ? '''
        if not days:
            return Response(
                {
                    "detail": "Invalid parameters. No time table data sent"
                },
                status = status.HTTP_400_BAD_REQUEST
            )

        ''' NOTE: Check if the section id is valid or not'''
        try:
            section_obj = Section.objects.get(section_id = section_id)
        except Section.DoesNotExist:
            return Response(
                {
                    "detail": "Invalid parameters. Section id is invalid"
                },
                status = status.HTTP_400_BAD_REQUEST
            )

        ''' NOTE: Update or Create time table data  '''
        for (day, periods) in days.items():

            ''' NOTE: Check if the day is valid or not ?'''
            try:
                day_obj = Day.objects.get(day = int(day))
            except Day.DoesNotExist:
                response_msg = f"Invalid day of the week i.e., {day}."
                return Response(
                    {
                        "detail": response_msg
                    },
                    status = status.HTTP_400_BAD_REQUEST
                )

            # for period in periods:

            for (period_no, period_data) in periods.items():

                is_online = period_data.get('is_online')
                subject_id = period_data.get('subject_id')
                teacher_id = period_data.get('teacher_id')
                timetable_date = period_data.get('timetable_date')
                '''
                    NOTE: check if is_online parameter is present or not 
                    
                    We will not check with "not" because is_online variable 
                    can be False and in that case the response will be wrong.
                '''
                if is_online == None:
                    response_msg = (
                        f"Invalid params in period_no {period_no}."
                        +
                        "'is_online' parameter is not present"
                    )
                    return Response(
                        {
                            "detail": response_msg
                        },
                        status = status.HTTP_400_BAD_REQUEST
                    )


                ''' NOTE: check if subject_id parameter is present or not '''
                if not subject_id:
                    response_msg = (
                        f"Invalid params in period_no {period_no}."
                        +
                        "'subject_id' parameter is not present"
                    )
                    return Response(
                        {
                            "detail": response_msg
                        },
                        status = status.HTTP_400_BAD_REQUEST
                    )

                ''' NOTE: Check if subject id is invalid or not'''
                try:
                    subject_obj = Subject.objects.get(subject_id = subject_id)
                except Subject.DoesNotExist:
                    response_msg = (
                        f"Invalid params in period_no {period_no}."
                        +
                        "subject_id is not valid"
                    )
                    return Response(
                        {
                            "detail": response_msg
                        },
                        status = status.HTTP_400_BAD_REQUEST
                    )


                ''' NOTE: check if teacher_id parameter is present or not '''
                if not teacher_id:
                    response_msg = (
                        f"Invalid params in period_no {period_no}. "
                        +
                        " teacher_id parameter is not present"
                    )
                    return Response(
                        {
                            "detail": response_msg
                        },
                        status = status.HTTP_400_BAD_REQUEST
                    )

                ''' NOTE: Check if teacher id is invalid or not'''
                try:
                    teacher_obj = Teacher.objects.get(classe_365_id = teacher_id)
                except Teacher.DoesNotExist:
                    response_msg = (
                        f"Invalid params in period_no {period_no}. "
                        +
                        f"teacher_id : {teacher_id} is not valid"
                    )
                    return Response(
                        {
                            "detail": response_msg
                        },
                        status = status.HTTP_400_BAD_REQUEST
                    )

                ''' NOTE: Check if period_no is valid or not ? '''
                try:
                    period_obj = Period.objects.get(period = int(period_no))
                except Period.DoesNotExist:
                    response_msg = f"Invalid period number i.e., {period_no}."
                    return Response(
                        {
                            "detail": response_msg
                        },
                        status = status.HTTP_400_BAD_REQUEST
                    )

                try:
                    is_period_already_exists = TimeTable.objects.get(
                        section__section_id = section_id,
                        day__day = int(day),
                        period_no__period = int(period_no)
                    )
                    is_period_already_exists.is_online = is_online
                    is_period_already_exists.subject = subject_obj
                    is_period_already_exists.teacher = teacher_obj

                    try:
                        is_period_already_exists.full_clean()
                    except ValidationError as err:
                        response_msg = f"Error: {err}"
                        logger.info(f"Error: {err}")
                        return Response(
                            {
                                "detail": response_msg
                            },
                            status = status.HTTP_400_BAD_REQUEST
                        )

                    is_period_already_exists.save()

                except TimeTable.DoesNotExist:

                    time_table_obj = TimeTable(
                        section = section_obj,
                        day = day_obj,
                        period_no = period_obj,
                        is_online = is_online,
                        subject = subject_obj,
                        teacher = teacher_obj,
                        timetable_date=timetable_date
                    )
                    try:
                        time_table_obj.full_clean()
                    except ValidationError as err:
                        response_msg = f"Error: {err}"
                        return Response(
                            {
                                "detail": response_msg
                            },
                            status = status.HTTP_400_BAD_REQUEST
                        )

                   # time_table_obj.save()
                    #time_table_obj.timetable_date=timetable_date
                    time_table_obj.save()

        return Response(
            {
                "detail": "Successfully Updated time table"
            },
            status = status.HTTP_200_OK
        )



#========================== New Update TimetableAPI ===============================#
class UpdateTimeTable2(APIView):
    ''' NOTE: Authenticating the user '''

    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        request_data = request.data
        logger.debug(f'request data - \n{request_data}')

        section_id = request_data[0].get('section_id')
        days = request_data[1].get('days')
        # week = request_data[2].get('week')
        # month = request_data[3].get('month')
        # year = request_data[4].get('year')
        ''' NOTE: Check if section id is sent ? '''
        if not section_id:
            return Response(
                {
                    "detail": "Invalid parameters. Section id is not sent"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        ''' NOTE: Check if time table data is sent ? '''
        if not days:
            return Response(
                {
                    "detail": "Invalid parameters. No time table data sent"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        ''' NOTE: Check if the section id is valid or not'''
        try:
            section_obj = Section.objects.get(section_id=section_id)
        except Section.DoesNotExist:
            return Response(
                {
                    "detail": "Invalid parameters. Section id is invalid"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        ''' NOTE: Update or Create time table data  '''
        for (day, periods) in days.items():

            ''' NOTE: Check if the day is valid or not ?'''
            try:
                day_obj = Day.objects.get(day=int(day))
            except Day.DoesNotExist:
                response_msg = f"Invalid day of the week i.e., {day}."
                return Response(
                    {
                        "detail": response_msg
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # for period in periods:

            for (period_no, period_data) in periods.items():

                is_online = period_data.get('is_online')
                subject_id = period_data.get('subject_id')
                teacher_id = period_data.get('teacher_id')
                week       = period_data.get('week')
                month      = period_data.get('month')
                year       = period_data.get('year')
                timetable_date=period_data.get('timetable_date')

                ''' NOTE :  disable to update of previous date's timetable .'''

                # get day,month,year's values from parameter's value
                timetable_date_values = timetable_date.split('-')
                pre_day = int(timetable_date_values[2])
                pre_month = int(timetable_date_values[1])
                pre_year = int(timetable_date_values[0])

                # get current day,month,year's values for set a condition
                curr_day = datetime.today().date().day
                curr_month = datetime.today().date().month
                curr_year = datetime.today().date().year


                if pre_day < curr_day and pre_month <= curr_month and pre_year <= curr_year:
                    response_msg = (
                            f"Nothing to update."
                            +
                            f" {pre_day}-{pre_month}-{pre_year} is  less from current date"
                    )
                    return Response(
                        {
                            "detail": response_msg
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                '''
                    NOTE: check if is_online parameter is present or not 

                    We will not check with "not" because is_online variable 
                    can be False and in that case the response will be wrong.
                                '''

                if is_online == None:
                    response_msg = (
                            f"Invalid params in period_no {period_no}."
                            +
                            "'is_online' parameter is not present"
                    )
                    return Response(
                        {
                            "detail": response_msg
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                ''' NOTE: check if subject_id parameter is present or not '''
                if not subject_id:
                    response_msg = (
                            f"Invalid params in period_no {period_no}."
                            +
                            "'subject_id' parameter is not present"
                    )
                    return Response(
                        {
                            "detail": response_msg
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                ''' NOTE: Check if subject id is invalid or not'''
                try:
                    subject_obj = Subject.objects.get(subject_id=subject_id)
                except Subject.DoesNotExist:
                    response_msg = (
                            f"Invalid params in period_no {period_no}."
                            +
                            "subject_id is not valid"
                    )
                    return Response(
                        {
                            "detail": response_msg
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                ''' NOTE: check if teacher_id parameter is present or not '''
                if not teacher_id:
                    response_msg = (
                            f"Invalid params in period_no {period_no}. "
                            +
                            " teacher_id parameter is not present"
                    )
                    return Response(
                        {
                            "detail": response_msg
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                ''' NOTE: Check if teacher id is invalid or not'''
                try:
                    teacher_obj = Teacher.objects.get(classe_365_id=teacher_id)
                except Teacher.DoesNotExist:
                    response_msg = (
                            f"Invalid params in period_no {period_no}. "
                            +
                            f"teacher_id : {teacher_id} is not valid"
                    )
                    return Response(
                        {
                            "detail": response_msg
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                ''' NOTE: Check if period_no is valid or not ? '''
                try:
                    period_obj = Period.objects.get(period=int(period_no))
                except Period.DoesNotExist:
                    response_msg = f"Invalid period number i.e., {period_no}."
                    return Response(
                        {
                            "detail": response_msg
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                try:
                    is_period_already_exists = TimeTable.objects.get(
                        section__section_id=section_id,
                        day__day=int(day),
                        period_no__period=int(period_no)
                    )
                    is_period_already_exists.is_online      = is_online
                    is_period_already_exists.subject        = subject_obj
                    is_period_already_exists.teacher        = teacher_obj
                    is_period_already_exists.timetable_week = week
                    is_period_already_exists.timetable_month= month
                    is_period_already_exists.timetable_year = year


                    try:
                        is_period_already_exists.full_clean()
                    except ValidationError as err:
                        response_msg = f"Error: {err}"
                        logger.info(f"Error: {err}")
                        return Response(
                            {
                                "detail": response_msg
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    is_period_already_exists.save()

                except TimeTable.DoesNotExist:

                    time_table_obj = TimeTable(
                        section=section_obj,
                        day=day_obj,
                        period_no=period_obj,
                        is_online=is_online,
                        subject=subject_obj,
                        teacher=teacher_obj,
                        timetable_week = week ,
                        timetable_month = month ,
                        timetable_year = year,
                        timetable_date=timetable_date
                    )
                    try:
                        time_table_obj.full_clean()
                    except ValidationError as err:
                        response_msg = f"Error: {err}"
                        return Response(
                            {
                                "detail": response_msg
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    time_table_obj.save()

        return Response(
            {
                "detail": "Successfully Updated time table"
            },
            status=status.HTTP_200_OK
        )
