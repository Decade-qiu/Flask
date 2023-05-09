
import datetime

time_limit = 5
x = (datetime.datetime.now()+datetime.timedelta(minutes=time_limit)).strftime("%Y-%m-%d %H:%M:%S")
print(type(datetime.datetime.now()))
print(type((datetime.datetime.now()+datetime.timedelta(minutes=time_limit))))
print(x)