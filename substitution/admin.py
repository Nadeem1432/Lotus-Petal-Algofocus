from django.contrib import admin
from substitution.models import Substitution
# Register your models here.
@admin.register(Substitution)
class SubstitutionAdmin(admin.ModelAdmin):

    list_display = (
        'get_section',
        'get_day',
        'get_period_no',
        'is_online',
        'get_subject',
        'get_teacher',
    )

    search_fields = (
        'section__claas__claas_id',
        'section__claas__claas_name',
        'section__section_id',
        'section__section_name',
        'day__day',
        'period_no__period',
        'is_online',
        'subject__subject_id',
        'subject__subject_name',
        'teacher__classe_365_id',
        'teacher__first_name',

    )


    # TODO: FORMFIELD POPULATION WHILE MAKEING ENTRIES
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == ''

    def get_section(self, obj):
        return obj.section.section_name

    def get_day(self, obj):
        return obj.day.day

    def get_period_no(self, obj):
        return obj.period_no.period

    def get_subject(self, obj):
        return obj.subject.subject_name

    def get_teacher(self, obj):
        return obj.teacher.first_name

