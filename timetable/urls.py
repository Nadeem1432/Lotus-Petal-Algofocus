
from django.urls import path

from timetable.views import (AllClassSection, AllTeacherSubject, GetTimeTable,
                             UpdateTimeTable , UpdateTimeTable2)

urlpatterns = [
    path(
        'get_time_table/',
        GetTimeTable.as_view(),
        name = 'get-time-table'
    ),
    path(
        'subject_teachers/',
        AllTeacherSubject.as_view(),
        name = 'all-teacher-subject'
    ),
    path(
        'all_claas_section/',
        AllClassSection.as_view(),
        name = 'all-claas-section'
    ),
    path(
        'update_timetable/',
        UpdateTimeTable2.as_view(),
        name = 'update_time_table'
    ),

    # old update timetable api
    path(
        'update_timetable2/',
        UpdateTimeTable.as_view(),
        name='update_time_table2'
    ),


]
