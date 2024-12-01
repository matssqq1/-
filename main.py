import telebot
from telebot import types
from src.test import taims
from api.parcer import parcer
import datetime
import json
import os

# dates and months
month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
days_list = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']


#вытаскиваем из масива часы и менуты для бота
a = taims()
start_hous = a[0]
start_minets = a[1]
ends_hous = a[2]
ends_minets = a[3]

bot = telebot.TeleBot('8130108661:AAES_8zx0x-fWAucFfUQ7GHTmFqV_WES5k4')

#end calculation command body/органа управления расчетами
menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
#para_ends = types.KeyboardButton("Время до каонца текущей пары")
#para_start = types.KeyboardButton("время до начала следующей пары")

menu.add(types.KeyboardButton("Пара"), types.KeyboardButton("Группа"))

back = types.ReplyKeyboardMarkup(resize_keyboard=True)
back_button = types.KeyboardButton("аим ис кам бек кхе кхе..")
back.add(back_button)

getter = parcer()
#start bot codding commands /start

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "привет!", reply_markup = menu)

#stop bot codding commands /stop (verigud is not deleted)

@bot.message_handler(commands=['stop'])
def message(message):
    bot.send_message(message.chat.id, "крашем бота...")
    bot.stop_polling()

@bot.message_handler(content_types=['text'])
def text_messages(message):
    start_hous_bot = start_hous
    start_minets_bot = start_minets
    ends_hous_bot = ends_hous
    ends_minets_bot = ends_minets

    if message.text[:4].lower() == 'пара':
        today = datetime.datetime.now()
        #today = today.replace(day=8, hour=0, minute=11) # DEBUG
        days_ago = 0

        group = parcer.read_users(message.chat.id)
        if group == -1:
            bot.send_message(message.chat.id, "У вас нет группы! Напишите команду Группа", reply_markup=menu)
            return

        for i in range(5):
            if getter.get_info(group, today) == 0:
                with open('cache/%s.json' % group, 'r') as file:
                    data = json.load(file)
                
                os.remove('cache/%s.json' % (group))

                date_call = "%s, %s %s" % (days_list[today.weekday()], today.day, month_list[today.month - 1])

                para_time = today
                

                para_ends_today = today
                para_ends_today = para_ends_today.replace(hour=int(data[len(data) - 1]['time-end'].split(':')[0]), minute=int(data[len(data) - 1]['time-end'].split(':')[1]))
                
                

                if para_ends_today < today and para_ends_today.day == today.day:
                    bot.send_message(message.chat.id, f"Сегодня пар нет! Последняя пара закончилась в: {data[len(data) - 1]['time-end']}", reply_markup=menu)

                    today = today + datetime.timedelta(days=1)
                    today = today.replace(hour=0, minute=0)

                for i in range(len(data)):
                    para_time = para_time.replace(hour=int(data[i]['time-start'].split(':')[0]), minute=int(data[i]['time-start'].split(':')[1]))

                    delta = para_time - today

                    if para_time > today:
                        if days_ago > 0:
                            bot.send_message(message.chat.id, f"Ближайшая пара через: {days_ago} дн\n{date_call}\n{data[i]['number']}, пройдёт: {data[i]['time-start']} - {data[i]['time-end']},\n{data[i]['subject']} {data[i]['teacher']} {data[i]['room']}", reply_markup=menu)
                        else:
                            bot.send_message(message.chat.id, f"Ближайшая пара через: {str(delta)[:5].split(':')[0]}ч {str(delta)[:5].split(':')[1]}м\n{date_call}\n{data[i]['number']}, пройдёт: {data[i]['time-start']} - {data[i]['time-end']},\n{data[i]['subject']} {data[i]['teacher']} {data[i]['room']}", reply_markup=menu)
                        return
                
            else:
                days_ago = days_ago + 1
                today = today + datetime.timedelta(days=1)
                today = today.replace(hour=0, minute=0)

        bot.send_message(message.chat.id, "в ближайшее время нет пар!", reply_markup=menu)

    elif message.text[:6].lower() == 'группа':
        bot.send_message(message.chat.id, "а теперь напиши свою группу!", reply_markup=menu)
        global change_group_flag
        change_group_flag = True
        
    elif change_group_flag == True:
        group = message.text
        if getter.write_users(message.chat.id, group) == -1:
            bot.send_message(message.chat.id, "Неккоректный формат группы, попробуйте еще раз! Формат в виде: 00.00.00", reply_markup=menu)
            return
        
        bot.send_message(message.chat.id, "группа сохранена", reply_markup=menu)
        #global change_group_flag
        change_group_flag = False

    # elif message.text == 'аим ис кам бек кхе кхе..':
    #     bot.send_message(message.chat.id, "Добро пожаловать обратно сударь каково ваше следующие желание", reply_markup=menu)
    # elif message.text == 'время до начала следующей пары':
    #     bot.send_message(message.chat.id, f"{start_hous_bot}:{start_minets_bot}", reply_markup=back)
    # elif message.text == 'Время до каонца текущей пары':
    #     bot.send_message(message.chat.id, f"{ends_hous_bot}:{ends_minets_bot}", reply_markup=back)
    else:
        bot.send_message(message.chat.id, "некорректная команда", reply_markup=menu)

bot.infinity_polling()
