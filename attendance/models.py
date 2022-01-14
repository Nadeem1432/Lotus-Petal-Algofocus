from datetime import date

from django.db import models
from timetable.models import TimeTable
from dashboard.models import Section


class StoreOfflineAttendance(models.Model):

    period = models.ForeignKey(TimeTable, on_delete=models.CASCADE)

    date = models.DateTimeField()

    attendance_status = models.JSONField()

    is_stored = models.BooleanField(default=True)

    is_marked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)


    @staticmethod
    def parse_date(dt):

        dt = list(map(int, dt.split('-')))

        return date(*dt)


class StoreOnlineAttendance(models.Model):

    uuid = models.CharField(unique=True, max_length=50)

    topic_name = models.CharField(max_length=100)

    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    period = models.ForeignKey(TimeTable, on_delete=models.CASCADE, blank = True, null = True)

    date = models.DateTimeField()

    attendance_status = models.JSONField(blank=True, null=True)

    wrong_emails = models.JSONField(blank=True, null=True)

    is_marked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)
