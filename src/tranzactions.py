import json
import os
import re

def log_write(log_name, text):
    file = open(log_name, 'a')
    file.write(text + '\n')
    file.close()

def write_users(chat_id, group):
    try:
        with open('data/users.json', 'r') as file: # read the json
            data = json.load(file)

        statement = True
        group = group.strip()

        # print(group) # проверка
        # pattern = r'^d{2}.d{2}.d{2}[п]?d?$'
        # #print(group)
        # # Проверяем соответствие
        # if re.search(pattern, group):
        #     pass
        # else:
        #     log_write('logs/user_changes.log', f"uncorrect transaction occured! user: {chat_id}, group: {group}")
        #     return -1
        
        for i in range(len(data)):
            #print(data[i])
            if data[i]['chat_id'] == chat_id:
                if data[i]['group'] != group:
                    data[i]['group'] = group
                    log_write('logs/user_changes.log', f"user: {chat_id} change group to: {group}")
                    statement = False
                    break
                statement = False
                break
        if statement:
            data.append({"chat_id": chat_id, "group": group})
            log_write('logs/user_changes.log', f"user: {chat_id} create profile, group: {group}")
        file = open('data/users.json', 'w')
        content = json.dumps(data)
        file.write(content)
        file.close()
    except Exception as e:
        log_write("logs/errors.log", str(e))
    

def json_read(json_name):
    try:
        with open(json_name, 'r') as file: # read the json
            data = json.load(file)
        os.remove(json_name)
        return data
    except Exception as e:
        log_write("logs/errors.log", str(e))

def read_users(chat_id):
    try:
        with open('data/users.json', 'r') as file: # read the json
            data = json.load(file)
        for i in range(len(data)):
            #print(data[i])
            if data[i]['chat_id'] == chat_id:
                return data[i]['group']
        return -1
    except Exception as e:
        log_write("logs/errors.log", str(e))