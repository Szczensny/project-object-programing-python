import datetime

# 2024-10-14 -- 2024-10-20
x = datetime.datetime(2024,10,17)
x = x.date()

monday = x - datetime.timedelta(days=x.weekday())
sunday = x + datetime.timedelta(days=(6 - x.weekday()))
print(x.weekday())
print(monday)
print(sunday)