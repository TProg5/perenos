import re
from datetime import datetime, timedelta


async def parse_time(time_string: str):
    match = re.search(r'/mute\s+(\d+)([smhd])', time_string)
    current_datetime = datetime.now()

    # if not match:
    #     return 'The command does not match the format: /mute X[s|m|h|d]'

    # Извлекаем число и единицу времени
    value = int(match.group(1))
    unit = match.group(2)

    match unit:
        case 'm':
            time_delta = timedelta(minutes=value)
            text = 'minute' if value == 1 else 'minutes'
        case 'h':
            time_delta = timedelta(hours=value)
            text = 'hour' if value == 1 else 'hours'
        case 'd':
            time_delta = timedelta(days=value)
            text = 'day' if value == 1 else 'days'
        case 'w':
            time_delta = timedelta(weeks=value)
            text = 'week' if value == 1 else 'weeks'
        case _:
            return None

    new_datetime = current_datetime + time_delta
    return new_datetime, text, value
