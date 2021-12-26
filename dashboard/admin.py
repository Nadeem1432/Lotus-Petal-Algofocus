from django.contrib import admin

from .models import (Claas, ClaasAlias, Section, Student, Subject,
                     Teacher, IncorrectTopic)


# import-export  pkg  import 
from import_export.admin import ExportMixin


# for filter feature
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter


@admin.register(Claas)
class ClaasAdmin(admin.ModelAdmin):
    list_display = (
        'claas_id',
        'claas_name',
    )

    search_fields = (
        'claas_id',
        'claas_name',
    )


@admin.register(ClaasAlias)
class ClaasAliasAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'claas'
    )


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = (
        'section_id',
        'section_name',
        'get_claas',
    )

    search_fields = (
        'section_id',
        'section_name',
        'claas__claas_id',
        'claas__claas_name',
    )

    def get_claas(self, obj):
        return obj.claas.claas_name

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        'subject_id',
        'subject_name',
        'section',
    )

    search_fields = (
        'subject_id',
        'subject_name',
        'section__section_id',
        'section__section_name',
        'section__claas__claas_id',
        'section__claas__claas_name',
    )


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        'classe_365_id',
        'email',
        'first_name',
        'last_name',
    )

    search_fields = (
        'classe_365_id',
        'email',
        'first_name',
        'last_name',
        'subjects__subject_id',
        'subjects__subject_name',
        'subjects__section__section_id',
        'subjects__section__section_name',
        'subjects__section__claas__claas_id',
        'subjects__section__claas__claas_name',
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'student_id',
        'admission_no',
        'email',
        'name',
        'section',
    )

    search_fields = (
        'student_id',
        'admission_no',
        'email',
        'name',
        'section__section_id',
        'section__section_name',
        'section__claas__claas_id',
        'section__claas__claas_name',
    )




@admin.register(IncorrectTopic)
class IncorrectTopicAdmin(ExportMixin , admin.ModelAdmin):
        # filter by date
    list_filter = (
        ('created_on', DateRangeFilter), ('updated_on', DateTimeRangeFilter),
                    )

    list_display = (
        'topic',
        'teacher_name',
        'meeting_time',
        'created_on',
        'updated_on',
        'meeting_id',
    )

    search_fields = (
        'topic',
        'teacher_name',
        'meeting_time',
        'meeting_id',
        'created_on',
    )


# @admin.register(IsAttendanceMarked)
# class IsAttendanceMarkedAdmin(admin.ModelAdmin):
#     list_display = (
#         'uuid',
#         'topic_name',
#         'meeting_time',
#         'is_marked',
#         'created_at',
#         'updated_at',
#         'student_json',
#     )

#     search_fields = (
#         'uuid',
#         'topic_name',
#         'is_marked',
#         'meeting_time',
#         'created_at',
#     )



# @admin.register(WrongEmail)
# class WrongEmailAdmin(admin.ModelAdmin):
#     list_display = (
#         'claas',
#         'topic',
#         'user_name',
#         'email',
#         'meeting_time',
#         'created_on',
#         'updated_on',
#         'meeting_uuid',
#     )

#     search_fields = (
#         'claas',
#         'topic',
#         'user_name',
#         'email',
#         'meeting_time',
#         'created_on',
#         'meeting_uuid',
#     )