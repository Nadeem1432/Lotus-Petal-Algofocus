from django.contrib import admin
from user_api.models import User

# admin.site.register(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'is_admin',
        'is_teacher',
        'is_student',
    )
    search_fields = (
        'username',
        'first_name',
        'last_name',
        'email',
    )

