import datetime
import api
'''
Checking the occurrence 
of the forecast 16 days
'''

border_day = 20
today = datetime.date.today()

def correct_date(date):
    i = [int(i) for i in date.split('.')]
    if (datetime.date(year=2020, month=i[0], day=i[1]) <= today + datetime.timedelta(days=15)) & (today <= datetime.date(year=2020, month=i[0], day=i[1])):
        select_day = datetime.date(year=2020, month=i[0], day=i[1])

        return what_days(select_day)
    else:
        return border_day

def what_days(select_day):
    """
    :return: number of days before the specified date
    """
    day = select_day - today
    api.send_weather(day.days)
    return day.days
