import parcer as parcer
import json
import datetime

#   "number": para[i],
#   "time": para[i+1],
#   "subject": para[i+2],
#   "teacher": para[i+3],
#   "room": para[i+4]

date = datetime.datetime.now() # date for get info

print(f"{date.day}:{date.weekday()}")

date2 = datetime.datetime.now()
date2 = date2.replace(hour='16', minute='10')
 
print(f"{date2.hour}:{date2.minute}")

# print(date < date2)

# getter = parcer.parcer() # create object for parcing(maybe i create other methods)
# 
# if getter.get_info("09.07.32", date) == 0: # check for errors and creating json
# 
#     with open('cache/09.07.32.json', 'r') as file: # read the json
#         data = json.load(file)
# 
#     for i in range(len(data)): # print the json
#         print(data[i])
# 
#     with open('data/users.json', 'r') as file: # read the json
#         data = json.load(file)
# 
#     for i in range(len(data)): # print the json
#         print(data[i])