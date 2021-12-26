from attendance.models import StoreOnlineAttendance, StoreOfflineAttendance
from django.contrib import admin


# for export feature
from import_export.admin import  ExportMixin

# for filter feature
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter



@admin.register(StoreOnlineAttendance)
class StoreOnlineAttendanceAdmin(ExportMixin,admin.ModelAdmin):
        # filter by date
    list_filter = (
        ('created_at', DateRangeFilter), ('updated_at', DateTimeRangeFilter),
                    )

    list_display = (
        'uuid',
        'is_marked',
        'topic_name',
        'date',
        'period',
        'get_section',        
        'attendance_status',
        'wrong_emails',
        'created_at',
        'updated_at',
    )

    search_fields = (
        'is_marked',
        'topic_name',
        'section__section_name',
    )

    def get_section(self, obj):
        return obj.section.section_name


@admin.register(StoreOfflineAttendance)
class StoreOfflineAttendanceAdmin(ExportMixin,admin.ModelAdmin):

    # filter by date
    list_filter = (
        ('created_at', DateRangeFilter), ('updated_at', DateTimeRangeFilter),
                    )

    list_display = (
        'period',
        'date',
        'is_stored',
        'is_marked',
        'created_at',
        'updated_at',
        'attendance_status',
    )

    # search_fields = (
    #     'period',
    # )

    # def get_period(self, obj):
    #     return obj.period

