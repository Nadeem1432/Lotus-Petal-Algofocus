from django.urls import path

from android_app.views import (GetAllStudentsOfAClass, GetAllTeachers,
                               GetTeacherClasses, StoreOfflineAttendanceStatus,GetClassAttendanceAPIView,GetOfflineAttendanceAPIView)


urlpatterns = [
    path('get_all_teachers/', GetAllTeachers.as_view(),
         name='get_all_teachers'),

    path('get_teacher_classes/', GetTeacherClasses.as_view(),
         name='get_teacher_classes'),

    path('get_all_students_of_class/', GetAllStudentsOfAClass.as_view(),
         name='get_all_students_of_class'),

    path('store_offline_attendance_status/', StoreOfflineAttendanceStatus.as_view(),
         name='store_offline_attendance_status'),

    path('get_period_attendance/',GetClassAttendanceAPIView.as_view(),
          name="get_period_attendance"),

    path('get_offline_attendance/',GetOfflineAttendanceAPIView.as_view(),
          name="get_offline_attendance")
]
