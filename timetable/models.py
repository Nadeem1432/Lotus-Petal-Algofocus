from datetime import datetime

from dashboard.models import Section, Subject, Teacher
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Day(models.Model):
    '''
        NOTE: VALUE FROM 0-6
        0 means monday, 1 means Tuesday and so on
    '''
    day = models.PositiveIntegerField(
        unique=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(6)
        ]
    )


    def __str__(self):
        return str(self.day)


class Period(models.Model):

    period = models.PositiveSmallIntegerField(
        unique=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(7)
        ]
    )

    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)


    def __str__(self):
        return str(self.period)


class TimeTable(models.Model):

    ''' The section with which the time table will be associated '''
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    '''  '''
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    '''  '''
    period_no = models.ForeignKey(Period, on_delete=models.CASCADE)
    '''  '''

    # TODO: TO ONLINE, OFFLINE AND BOTH
    is_online = models.BooleanField(default=False)

    substituted = models.BooleanField(default=False)

    '''  '''
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    '''  '''
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    ''' updates in timetable 28 oct 2021 '''

    timetable_date   = models.DateField(blank=True,null=True)

    '''example : January , February  .....'''
    timetable_month  = models.IntegerField(blank=True, null=True)


    ''' example : 2021 , 2022 '''
    timetable_year   = models.IntegerField(blank=True, null=True)

    '''example : Week 1 , Week 2 .....'''
    timetable_week    = models.IntegerField(blank=True, null=True)


    class Meta:
        unique_together = (
            'day',
            'period_no',
            'section',
        )

    @staticmethod
    def find_day_of_week():
        '''
            give us the day of the week in number (range 0-6)
            monday = 0, tuesday = 1 and so on ...
        '''
        day_of_week_in_num = datetime.today().weekday()
        # day_of_week = week_day_maping[day_of_week_in_num]

        return day_of_week_in_num


    def clean(self):
        try:
            qs = Teacher.objects.get(
                classe_365_id = self.teacher.classe_365_id,
                subjects__subject_id = self.subject.subject_id
            )
        except Teacher.DoesNotExist:
            message = "This Teacher & Subject mapping is invalid !!"
            raise ValidationError(message)









