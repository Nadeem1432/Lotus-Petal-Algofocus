import csv
from datetime import datetime, timedelta

from django.http.response import HttpResponse

from attendance.models import StoreOnlineAttendance
from dashboard.models import IncorrectTopic


def export_incorrect_topics_csv(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="incorrect_topics.csv"'

    writer = csv.writer(response)

    writer.writerow([ 'topic', 'meeting_time', 'teacher_name', 'meeting_id' ])

    start_date = datetime(2021, 9, 13) 
    end_date = datetime(2021, 9, 26)

    qs = IncorrectTopic.objects.filter(
        meeting_time__gte = start_date,
        meeting_time__lte = end_date,
    )

    for i in qs:
        writer.writerow([
            i.topic,
            i.meeting_time.date(),
            i.teacher_name,
            i.meeting_id,
        ])

    return response


def export_wrong_emails_csv(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="wrong_emails.csv"'

    writer = csv.writer(response)

    writer.writerow([
        'uuid',
        'topic_name',
        'section',
        'date',
        'wrong_emails',
    ])

    qs = StoreOnlineAttendance.objects.filter(
        is_marked = True,
    )

    for i in qs:
        writer.writerow([
            i.uuid,
            i.topic_name,
            i.section,
            i.date.date(),
            i.wrong_emails,
        ])

    return response
