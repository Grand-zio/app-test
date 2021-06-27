import time


def get_time_struct():
    time_struct = time.localtime(time.time())
    tm_year = str(time_struct.tm_year)
    tm_mon = str(time_struct.tm_mon)
    tm_mday = str(time_struct.tm_mday)
    tm_hour = str(time_struct.tm_hour)
    tm_min = str(time_struct.tm_min)
    tm_sec = str(time_struct.tm_sec)
    test_time = tm_year + tm_mon + tm_mday + tm_hour + tm_min + tm_sec
    return test_time
