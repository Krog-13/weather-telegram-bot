MAX_MONTH_YEAR = 13
MAX_DAYS_MONTH = 32
LEN_FORMAT_MM_DD = 2

def check_data(date):
    days = [i for i in range(1,MAX_DAYS_MONTH)]
    month = [i for i in range(1,MAX_MONTH_YEAR)]
    try:
        a = [int(i) for i in date.split('.')]
        if len(a) > LEN_FORMAT_MM_DD:
            return False
        if not ((a[0] in month) and (a[1] in days)):
            return False
    except ValueError:
        return False
    except IndexError:
        return False
    else:
        return True



