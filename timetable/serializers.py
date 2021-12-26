from rest_framework import serializers

from dashboard.models import Claas, Section, Subject, Teacher
from timetable.models import TimeTable


class AllClaasSectionSerializer(serializers.ModelSerializer):

    claas_id = serializers.SerializerMethodField()

    claas_name = serializers.SerializerMethodField()

    sections = serializers.SerializerMethodField()


    class Meta:
        model = Claas
        fields = (
            'claas_id',
            'claas_name',
            'sections',
        )

    def get_claas_id(self, obj):
        return obj.claas_id

    def get_claas_name(self, obj):
        return obj.claas_name

    def get_sections(self, obj):
        sections_qs = Section.objects.filter(
            claas__claas_id = obj.claas_id
        )
        section_serialized = SectionsSerializer(
            sections_qs,
            many = True,
        )
        section_serialized_data = section_serialized.data

        return section_serialized_data


class SectionsSerializer(serializers.ModelSerializer):

    section_id = serializers.SerializerMethodField()

    section_name = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = (
            'section_id',
            'section_name',
        )

    def get_section_id(self, obj):
        return obj.section_id

    def get_section_name(self, obj):
        return obj.section_name


class AllSubjectTeacherSerializer(serializers.ModelSerializer):

    subject_id = serializers.SerializerMethodField()

    subject_name = serializers.SerializerMethodField()

    teachers = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = (
            'subject_id',
            'subject_name',
            'teachers',
        )

    def get_subject_id(self, obj):
        return obj.subject_id

    def get_subject_name(self, obj):
        return obj.subject_name

    def get_teachers(self, obj):

        teachers_qs = Teacher.objects.filter(
            subjects__subject_id = obj.subject_id
        )

        teachers_serialized = TeacherSerializer(
            teachers_qs,
            many = True
        )

        teachers_serialized_data = teachers_serialized.data

        return teachers_serialized_data


class TeacherSerializer(serializers.ModelSerializer):

    id = serializers.SerializerMethodField()

    name = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = (
            'id',
            'name',
        )

    def get_id(self, obj):
        return obj.classe_365_id

    def get_name(self, obj):
        return obj.first_name


class TimeTableSerializer(serializers.ModelSerializer):

    day = serializers.SerializerMethodField()

    period_no = serializers.SerializerMethodField()

    is_online = serializers.SerializerMethodField()

    subject_id = serializers.SerializerMethodField()

    subject = serializers.SerializerMethodField()

    teacher_id = serializers.SerializerMethodField()

    teacher = serializers.SerializerMethodField()

    timetable_date = serializers.SerializerMethodField()

    class Meta:
        model = TimeTable
        fields = (
            'day',
            'period_no',
            'is_online',
            'subject_id',
            'subject',
            'teacher_id',
            'teacher',
            'id',
            'timetable_date'
        )

    def get_day(self, obj):
        return obj.day.day

    def get_period_no(self, obj):
        return obj.period_no.period

    def get_is_online(self, obj):
        return obj.is_online

    def get_subject_id(self, obj):
        return obj.subject.subject_id

    def get_subject(self, obj):
        return obj.subject.subject_name

    def get_teacher_id(self, obj):
        return obj.teacher.classe_365_id

    def get_teacher(self, obj):
        return obj.teacher.first_name

    def get_timetable_date(self, obj):
        return obj.timetable_date
