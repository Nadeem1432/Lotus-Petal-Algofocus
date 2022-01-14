from django.contrib import admin
from .models import TimeTable, Day, Period

# admin.site.register(Substitution)


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):

    list_display = (

        'day_name',
        'day'
    )


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):

    list_display = (
        'period',
        'start_time',
        'end_time',
    )


@admin.register(TimeTable)
class TimeTableAdmin(admin.ModelAdmin):

    list_display = (
        'get_class_section',
        'get_section_id',
        'get_date',
        'get_day',
        'get_period_no',
        'get_subject',
        'get_teacher',
        'is_online',
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

    # def get_class_section(self, obj):
    #     return obj.section.section_name

    def get_class_section(self, obj):
        return f'{obj.section.claas.claas_name} - {obj.section.section_name}'

    def get_section_id(self, obj):
        return obj.section.section_id

    def get_date(self, obj):
        return obj.timetable_date

    def get_day(self, obj):
        return obj.day.day_name

    def get_period_no(self, obj):
        return obj.period_no.period

    def get_subject(self, obj):
        return obj.subject.subject_name


    def get_teacher(self, obj):
        return obj.teacher.first_name



    #Renames column head
    get_class_section.short_description = 'Class - Section'
    get_section_id.short_description = 'Section Id'
    get_day.short_description = 'Day'
    get_period_no.short_description = 'Period'
    get_subject.short_description = 'Subject'
    get_teacher.short_description = 'Teacher'
    get_date.short_description = 'Date'

    # Allows column order sorting
    get_date.admin_order_field  = 'timetable_date'
