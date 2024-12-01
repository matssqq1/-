import requests
import os
class parcer:
    

    def __init__(self):
        pass
    def get_info(self, group, date):
        url = 'https://расписание.нхтк.рф/%s.html#заголовок' % (group) # url для второй страницы
        r = requests.get(url)
        
        with open('cache/%s.html' % (group), 'w') as output_file:
            output_file.write(r.text.encode('cp1251'))
