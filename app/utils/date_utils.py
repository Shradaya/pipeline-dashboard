import datetime

def convert_date_to_string(value, date_format = "%m/%d/%Y"):
    if not isinstance(value, datetime.date) and not isinstance(value, datetime.datetime):
        return None
    return value.strftime(date_format)

def convert_string_to_date(value, date_format = "%m/%d/%Y"):
    if not value:
        return None
    try:
        return datetime.datetime.strptime(value, date_format)
    except:
        return None
    