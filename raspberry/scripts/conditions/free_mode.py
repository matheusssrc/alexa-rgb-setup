from conditions.work_mode import is_work_mode

def is_free_mode():
    return not is_work_mode()