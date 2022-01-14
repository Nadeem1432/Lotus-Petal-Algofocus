from django.urls import path , include
from .views import home, privacy, index ,timetable,attendance , ChangePasswordView



urlpatterns = [
    path("", index, name="index"),
    path("timetable",timetable,name="time-table"),
    path("attendance",attendance,name='attendance'),

    # urls of allauth
    path('accounts/', include("allauth.urls") , name="accounts" ),

    path('change_password', ChangePasswordView.as_view(), name='ChangePasswordView'),
    path('dashboard', home ,  name ='home'),
    path('privacy', privacy, name='privacy'),

]
