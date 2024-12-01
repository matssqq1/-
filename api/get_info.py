import requests
import codecs
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

        print(response.text)

        out_file = codecs.open('cache/%s.html' % (group), 'w', 'utf-8')
        out_file.write(response.text)
        out_file.close()
