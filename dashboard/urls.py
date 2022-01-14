from django.urls import path

from .views import export_incorrect_topics_csv, export_wrong_emails_csv


urlpatterns = [
    path('export_incorrect_topics', export_incorrect_topics_csv, name = 'export-incorrect-topics'),
    path('export_wrong_emails', export_wrong_emails_csv, name = 'export-wrong-emails'),
]