from datetime import datetime


def toDateObj(date_string: str) -> datetime:
    """
    Take a date string and return a date object

    params:
        - date_string (str) - string to convert to datetime object
    returns:
        - datetime - coverted datetime object
    """
    return datetime.strptime(date_string, "%Y-%m-%d %H:%M")
