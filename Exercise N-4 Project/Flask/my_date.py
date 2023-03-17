from datetime import datetime


def date_difference(current_date, creation_date):
    current_date = datetime.strptime(current_date, "%Y-%m-%d")
    creation_date = datetime.strptime(creation_date, "%Y-%m-%d")
    result = current_date - creation_date
    return int(result.days)

