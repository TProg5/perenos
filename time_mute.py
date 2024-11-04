import re
from datetime import datetime, timedelta


def parse_time(time_string):
    time_string = time_string[6:]
    match_ = re.match(r"(\d+)([a-z])", time_string.lower().strip())
    current_datetime = datetime.now()

    if match_:
        value, unit = int(match_.group(1)), match_.group(2)

        match unit:
            case 'm': time_delta = timedelta(minutes=value)
            case 'h': time_delta = timedelta(hours=value)
            case 'd': time_delta = timedelta(days=value)
            case 'w': time_delta = timedelta(weeks=value)
            case _: return None

        new_datetime = current_datetime + time_delta
        return new_datetime


def parse_block(string):
    value = string[8:9]
    match value:
        case 'm':
            value = 'minute'
        case 'h':
            value = 'hour'
        case 'd':
            value = 'day'
        case 'w':
            value = 'week'
        case _:
            return None

    return value
