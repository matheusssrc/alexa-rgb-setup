from datetime import datetime, time

def is_work_mode():
    now = datetime.now()
    is_weekday = now.weekday() < 5
    is_working_hour = time(8, 0) <= now.time() <= time(17, 0)
    return is_weekday and is_working_hour