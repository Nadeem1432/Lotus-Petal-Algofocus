from django.urls import path
from .views import  home , privacy , index ,timetable,attendance



urlpatterns = [
    path("", index, name="index"),
    path("timetable",timetable,name="time-table"),
    path("attendance",attendance,name='attendance'),

    # path('', home ,  name ='home'),
    path('privacy', privacy, name='privacy'),

]
