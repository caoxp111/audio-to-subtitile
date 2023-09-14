import datetime


# 格式：00:00:56,400
def trans_ts(time_str):
    time_sec = float(time_str)
    delta = datetime.timedelta(seconds=time_sec)
    time_formatted = (datetime.datetime.min + delta).strftime('%H:%M:%S,%f')[:-3]
    return time_formatted
