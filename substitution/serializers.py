from rest_framework import serializers

from dashboard.models import Claas, Section, Subject, Teacher
from timetable.models import TimeTable
from substitution.models import Substitution



class SubstitutionSerializer(serializers.ModelSerializer):

    day = serializers.SerializerMethodField()

    period_no = serializers.SerializerMethodField()

    is_online = serializers.SerializerMethodField()

    subject_id = serializers.SerializerMethodField()

    subject = serializers.SerializerMethodField()

    teacher_id = serializers.SerializerMethodField()

    teacher = serializers.SerializerMethodField()

    substitution_date = serializers.SerializerMethodField()

    class Meta:
        model = Substitution
        fields = (
            'day',
            'period_no',
            'is_online',
            'subject_id',
            'subject',
            'teacher_id',
            'teacher',
            'id',
            'substitution_date'
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

    def get_substitution_date(self, obj):
        return obj.substitution_date



class AddSubstitutionSerializer(serializers.Serializer):
    section_id              =  serializers.CharField(max_length = 10)
    subject_id              =  serializers.CharField(max_length = 10)
    teacher_id              =  serializers.CharField(max_length = 10)
    period_no               =  serializers.CharField(max_length = 10)
    substitution_date       =  serializers.CharField(max_length = 15)

    class Meta:
        fields = ['section_id' , 'subject_id','teacher_id','period_no','substitution_date']



class GetSubstitutionSerializer(serializers.Serializer):
    section_id              =  serializers.CharField(max_length = 10)
    substitution_date       =  serializers.CharField(max_length = 15)

    class Meta:
        fields = ['section_id' ,'substitution_date']

