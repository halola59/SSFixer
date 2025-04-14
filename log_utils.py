# log_utils.py
def CLOG(clogger, file, row, condition, action):
    clogger.info(f"{file};{row};{condition};{action}")
