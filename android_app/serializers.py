from datetime import datetime
from rest_framework import serializers

from attendance.models import StoreOfflineAttendance
from dashboard.models import Student, Teacher
from timetable.models import TimeTable
from substitution.models import Substitution


class TeacherClassSerializer(serializers.ModelSerializer):

    id = serializers.SerializerMethodField()
    claas = serializers.SerializerMethodField()
    section_id = serializers.SerializerMethodField()
    section = serializers.SerializerMethodField()
    period_number = serializers.SerializerMethodField()
    period_start_time = serializers.SerializerMethodField()
    period_end_time = serializers.SerializerMethodField()
    subject_id = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()
    is_online = serializers.SerializerMethodField()
    substituted = serializers.SerializerMethodField()
    is_stored = serializers.SerializerMethodField()
    timetable_date = serializers.SerializerMethodField()

    class Meta:
        model = TimeTable
        fields = (
            'id',
            'claas',
            'section_id',
            'section',
            'period_number',
            'period_start_time',
            'period_end_time',
            'subject_id',
            'subject',
            'is_online',
            'is_stored',
            'timetable_date',
            'substituted'

        )


    def get_id(self, obj):
        return obj.id

    def get_claas(self, obj):
        return obj.section.claas.claas_name

    def get_section_id(self, obj):
        return obj.section.section_id
        
    def get_section(self, obj):
        return obj.section.section_name

    def get_period_number(self, obj):
        return obj.period_no.period

    def get_period_start_time(self, obj):
        return obj.period_no.start_time

    def get_period_end_time(self, obj):
        return obj.period_no.end_time

    def get_subject_id(self, obj):
        return obj.subject.subject_id

    def get_subject(self, obj):
        return obj.subject.subject_name

    def get_is_online(self, obj):
        return obj.is_online

    def get_is_stored(self, obj):

        try:
            StoreOfflineAttendance.objects.get(
                period__id = obj.id,
                date__date = datetime.now()
            )
            return True
        except StoreOfflineAttendance.DoesNotExist:
            return False

    def get_timetable_date(self, obj):
        return obj.timetable_date

    def get_substituted(self, obj):
        return obj.substituted




class SubstitutionTeacherClassSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    claas = serializers.SerializerMethodField()
    section_id = serializers.SerializerMethodField()
    section = serializers.SerializerMethodField()
    period_number = serializers.SerializerMethodField()
    period_start_time = serializers.SerializerMethodField()
    period_end_time = serializers.SerializerMethodField()
    subject_id = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()
    is_online = serializers.SerializerMethodField()
    substituted = serializers.SerializerMethodField()
    is_stored = serializers.SerializerMethodField()
    substitution_date = serializers.SerializerMethodField()

    class Meta:
        model = Substitution
        fields = (
            'id',
            'claas',
            'section_id',
            'section',
            'period_number',
            'period_start_time',
            'period_end_time',
            'subject_id',
            'subject',
            'is_online',
            'substituted',
            'is_stored',
            'substitution_date'
        )

    def get_id(self, obj):
        return obj.id

    def get_claas(self, obj):
        return obj.section.claas.claas_name

    def get_section_id(self, obj):
        return obj.section.section_id

    def get_section(self, obj):
        return obj.section.section_name

    def get_period_number(self, obj):
        return obj.period_no.period

    def get_period_start_time(self, obj):
        return obj.period_no.start_time

    def get_period_end_time(self, obj):
        return obj.period_no.end_time

    def get_subject_id(self, obj):
        return obj.subject.subject_id

    def get_subject(self, obj):
        return obj.subject.subject_name

    def get_is_online(self, obj):
        return obj.is_online


    def get_substituted(self, obj):
        return obj.substituted

    def get_is_stored(self, obj):

        try:
            StoreOfflineAttendance.objects.get(
                period__id=obj.id,
                date__date=datetime.now()
            )
            return True
        except StoreOfflineAttendance.DoesNotExist:
            return False

    def get_substitution_date(self, obj):
        return obj.substitution_date


class GetAllTeachersSerializer(serializers.ModelSerializer):

    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = ('id', 'name', 'email',)

    def get_id(self, obj):
        return obj.classe_365_id

    def get_name(self, obj):
        return obj.first_name + ' ' + obj.last_name

    def get_email(self, obj):
        return obj.email


class GetAllStudentsOfAClassSerializer(serializers.ModelSerializer):

    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ('id', 'name',)

    def get_id(self, obj):
        # return obj.student_id
        return obj.admission_no

    def get_name(self, obj):
        return obj.name
