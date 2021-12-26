
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from timetable.models import TimeTable
# from .models import (Claas, IsAttendanceMarked, Section, Student, Subject,
#                      Teacher)
# from .serializers import (ClaasSerializer, IsAttendanceMarkedSerializer,
#                           SectionSerializer, StudentSerializer,
#                           SubjectSerializer, TeacherClassSerializer,
#                           TeacherSerializer)



'''
    NOTE: API to get all the classes to be held today by a teacher.
'''
# class GetTeacherClasses(APIView):
#     # TODO: PUT AUTHENTICATION CLASSES

#     def post(self, request, *args, **kwargs):

#         request_data = request.data

#         teacher_classe_365_id = request_data.get('teacher_id')

#         ''' NOTE: To get the day of the week '''
#         day_of_week = TimeTable.find_day_of_week()

#         ''' NOTE: Filter all the classes to be held today of a teacher'''
#         all_classes_of_today_qs = TimeTable.objects.filter(
#             teacher__classe_365_id=teacher_classe_365_id,
#             day__day=day_of_week,
#         )

#         ''' NOTE: Serialize data to be sent to the user '''
#         serialized_data = TeacherClassSerializer(
#             all_classes_of_today_qs,
#             many=True
#         )

#         # if not serialized_data.is_valid():
#         serialized_data = serialized_data.data

#         return Response(serialized_data, status=status.HTTP_200_OK)




# class ClaasList(viewsets.ModelViewSet):
#     queryset = Claas.objects.all()
#     serializer_class = ClaasSerializer


# class SectionList(viewsets.ModelViewSet):
#     queryset = Section.objects.all()
#     serializer_class = SectionSerializer


# class SubjectList(viewsets.ModelViewSet):
#     queryset = Subject.objects.all()
#     serializer_class = SubjectSerializer


# class TeacherList(viewsets.ModelViewSet):
#     queryset = Teacher.objects.all()
#     serializer_class = TeacherSerializer


# class StudentList(viewsets.ModelViewSet):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer


# class IsAttendanceMarkedList(viewsets.ModelViewSet):
#     queryset = IsAttendanceMarked.objects.all()
#     serializer_class = IsAttendanceMarkedSerializer
