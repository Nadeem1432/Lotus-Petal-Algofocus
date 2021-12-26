from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls, name='adminpage'),
    path('api/v1/', include('android_app.urls')),
    path('api/v1/', include('timetable.urls')),
    path('api/v1/', include('user_api.urls')),
    path('api/v1/', include('dashboard.urls')),
    path('api/v1/', include('substitution.urls')),
    path('', include('UI.urls')),
]
