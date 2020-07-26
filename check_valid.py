
def check_data(date):
    days = [i for i in range(1,32)]
    month = [i for i in range(1,13)]
    try:
        a = [int(i) for i in date.split('.')]
        if len(a) > 2:
            return False
        if not ((a[0] in month) and (a[1] in days)):
            return False
    except ValueError:
        return False
    else:
        return True



