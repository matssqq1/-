import requests
import codecs
from bs4 import BeautifulSoup
import json
import datetime
import os

class parcer:
    

    def __init__(self):
        pass
    def get_info(self, group, date):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
        }
        url = 'https://расписание.нхтк.рф/%s.html#заголовок' % (group) # url для второй страницы
        response = requests.get(url=url, headers=headers)
        response.encoding = response.apparent_encoding

        #print(response.text)

        out_file = codecs.open('cache/%s.html' % (group), 'w', 'utf-8')
        out_file.write(response.text)
        out_file.close()

        html_file = codecs.open('cache/%s.html' % (group), 'r', 'utf-8')
        soup = BeautifulSoup(html_file.read(), 'html.parser')
        html_file.close()
        
        os.remove('cache/%s.html' % (group))

        month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
        days_list = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

        date_call = "%s, %s %s" % (days_list[date.weekday()], date.day, month_list[date.month - 1]) # date to format: Суббота, 7 декабря

        delete_list = ['\xad', '\n', '\xa0']
        change_list = ['', '|', ' ']

        day = soup.select("tr")

        result_rows = []
        out_rows = []
        para = []

        for stroke in day:
            s = stroke.text

            for i in range(len(delete_list)):
                s = s.replace(delete_list[i], change_list[i])
            
            result_rows.append(s)
        
        search_state = False

        for i in range(len(result_rows)): # base HTML to list parcing
            if result_rows[i] == date_call:
                search_state = True
                i += 1

            if search_state == True and result_rows[i] != 'ВремяПредметПреподавательПрепод.Ауд.':
                out_rows.append(result_rows[i])
            
            if result_rows[i].split(',')[0] in days_list and search_state == True:
                search_state = False

        #print(out_rows)

        for i in range(len(out_rows)): # final list parcing
            for j in range(len(out_rows[i].split('|'))):
                buff = out_rows[i].split('|')[j]

                if j == 1: # time parcing
                    para.append(buff[:1])

                    buff = buff[1:]
                    if len(buff) > 21:
                        buff = buff[:len(buff) - 11]
                    else:
                        buff = buff[:len(buff) - 10]
                    para.append(buff.split(' ')[0])
                    continue

                if buff != '':
                    para.append(buff)
        try:
            para.pop(len(para) - 1)
        except:
            return -1

        # print(para[1])
        # print(para[1].split('–')[1])

        objects = [] # json write
        for i in range(0, len(para), 5):
            obj = {
                "number": para[i],
                "time-start": para[i+1].split('–')[0],
                "time-end": para[i+1].split('–')[1],
                "subject": para[i+2],
                "teacher": para[i+3],
                "room": para[i+4]
            }
            objects.append(obj)

        # objects to json
        json_string = json.dumps(objects, ensure_ascii=False)

        json_file = open('cache/%s.json' % (group), 'w')
        json_file.write(json_string)
        json_file.close()

        return 0
    
    
    def read_users(chat_id):
        with open('data/users.json', 'r') as file: # read the json
            data = json.load(file)

        for i in range(len(data)):
            #print(data[i])
            if data[i]['chat_id'] == chat_id:
                return data[i]['group']
        
        return -1
    
    def write_users(self, chat_id, group):
        with open('data/users.json', 'r') as file: # read the json
            data = json.load(file)
        
        statement = True

        for i in range(len(data)):
            #print(data[i])
            if data[i]['chat_id'] == chat_id:
                if data[i]['group'] != group:
                    data[i]['group'] = group
                    statement = False
                    break
                statement = False
                break

        if statement:
            data.append({"chat_id": chat_id, "group": group})

        file = open('data/users.json', 'w')
        content = json.dumps(data)
        file.write(content)
        file.close()
