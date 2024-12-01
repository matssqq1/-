import datetime
from datetime import datetime
# from test import taims
# # now = datetime.now()
# # target_time = datetime(now.year, now.month, now.day, 16, 10)
# # time_difference = target_time - now
# # x_ends_hours = time_difference.seconds // 3600
# # minutes = (time_difference.seconds % 3600) // 60
# # print(f"До 16:10 осталось {x_ends_hours} часов и {minutes} минут")
# # print(taims())
# # b = a // 100
# # s = a % 100
# # while s > 60:
# #     b = b + 1
# #     s = s -60
# # print(b,":",s)
# a = taims()
# start_hous = a[0]
# start_minets = a[1]
# ends_hous = a[2]
# ends_minets = a[3]
# print(start_hous,start_minets,ends_hous,ends_minets)
today = datetime.now()
tomorrow = today + datetime.timedelta(days=1)
print(tomorrow)
