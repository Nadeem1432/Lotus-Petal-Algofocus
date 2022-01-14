
from datetime import datetime


def fetch_date_time(date_time):
    ''' received format : 2021-08-06T03:09:31Z '''

    date, time = date_time.split('T')
    
    date = list(map(int, date.split('-')))
    time = time[:8]
    time = list(map(int, time.split(':')))

    new_date_time = date + time

    return datetime(*new_date_time)


# print(fetch_date_time('2021-08-06T03:09:31Z'))