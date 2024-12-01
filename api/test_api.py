import get_info
import json
import datetime

# 1 - para num
# 2 - para time
# 3 - para name
# 4 - prepod
# 5 - room

date = datetime.date(2024, 12, 2) # date for get info

getter = get_info.parcer() # create object for parcing(maybe i create other methods)

if getter.get_info("09.07.32", date) == 0: # check for errors and creating json

    with open('cache/09.07.32.json', 'r') as file: # read the json
        data = json.load(file)

    for i in range(len(data)): # print the json
        print(data[i])