import datetime
'''
Show day of the week
'''
weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
today = datetime.datetime.now().date()
thisXMasDay = today.weekday()
day_of_week = weekDays[thisXMasDay]
