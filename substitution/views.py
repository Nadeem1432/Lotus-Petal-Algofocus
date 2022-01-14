from django.shortcuts import render
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
from substitution.models import Substitution
from datetime import datetime
from substitution.serializers import SubstitutionSerializer , AddSubstitutionSerializer , GetSubstitutionSerializer

# logger config
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s-%(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


class GetSubstitution(APIView):

    ''' NOTE: Authenticating the user '''
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = GetSubstitutionSerializer

    def post(self, request, *args, **kwargs):
        serializer = GetSubstitutionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        else:
            request_data = serializer.data
            section_id              = request_data.get('section_id', 'section_id not found!!!')
            substitution_date       = request_data.get('substitution_date', 'section_id not found!!!')


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
                                                 )

            if not section_obj:
                return Response(
                    {
                        "detail": "Invalid parameters. Section id is invalid"
                    },
                    status = status.HTTP_400_BAD_REQUEST
                )

            substitution_qs = Substitution.objects.filter(
                    section__section_id = section_id,
                    substitution_date = substitution_date,

            )

            substitution_serialized = SubstitutionSerializer(
                substitution_qs,
                many = True
            )

            substitution_serialized_data = substitution_serialized.data

            return Response(
                substitution_serialized_data,
                status = status.HTTP_200_OK
            )






class Addsubstitution(APIView):
    ''' NOTE: Authenticating the user '''

    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = AddSubstitutionSerializer
    def post(self, request, *args, **kwargs):

        serializer = AddSubstitutionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        else:
            request_data = serializer.data
            section_id          = request_data.get('section_id', 'section_id not found!!!')
            subject_id          = request_data.get('subject_id', 'subject_id not found!!!')
            teacher_id          = request_data.get('teacher_id', 'teacher_id not found!!!')
            period_no           = request_data.get('period_no', 'period_no not found!!!')
            substitution_date   = request_data.get('substitution_date', 'subject_id not found!!!')

        # request_data = request.data
        # logger.debug(f'request data - \n{request_data}')
        #
        # section_id        = request_data.get('section_id')
        # subject_id        = request_data.get('subject_id')
        # teacher_id        = request_data.get('teacher_id')
        # period_no         = request_data.get('period_no')
        # substitution_date = request_data.get('substitution_date')



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



        ''' NOTE: Check if the subject id is valid or not'''
        try:
            subject_obj = Subject.objects.get(subject_id=subject_id)
        except Subject.DoesNotExist:
            return Response(
                {
                    "detail": "Invalid parameters. Subject id is invalid"
                },
                status=status.HTTP_400_BAD_REQUEST
            )



        ''' NOTE: Check if the teacher id is valid or not'''
        try:
            teacher_obj = Teacher.objects.get(classe_365_id=teacher_id)
        except Teacher.DoesNotExist:
            return Response(
                {
                    "detail": "Invalid parameters. Teacher id is invalid"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        ''' NOTE: Check if the Period no valid or not'''
        try:
            period_obj = Period.objects.get(period=int(period_no))
        except Period.DoesNotExist:
            return Response(
                {
                    "detail": "Invalid parameters. Period no is invalid"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        ''' Get current Day '''
        day = int(datetime.today().weekday())
        ''' NOTE: Check if the Day valid or not'''
        try:
            day_obj = Day.objects.get(day=day)
        except Day.DoesNotExist:
            return Response(
                {
                    "detail": "Invalid parameters. Day is invalid"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            substitution_obj = Substitution(
                                            section=section_obj,
                                            day=day_obj,
                                            period_no=period_obj,
                                            subject=subject_obj,
                                            teacher=teacher_obj,
                                            is_online=False,
                                            substitution_date=substitution_date
                                        )
            substitution_obj.save()
            return Response(
                                {
                                    "detail": "Successfully created substitution"
                                },
                                status=status.HTTP_200_OK
                            )


        except Exception as e:
            return Response(
                {
                    "detail": f"{e}"
                },
                status=status.HTTP_400_BAD_REQUEST
            )






