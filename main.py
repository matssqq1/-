import telebot
from telebot import types
# from src.test import taims
from api.parcer import parcer
import src.tranzactions as trnz
import datetime
# import json


month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
days_list = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

bot = telebot.TeleBot('8130108661:AAES_8zx0x-fWAucFfUQ7GHTmFqV_WES5k4')

menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(types.KeyboardButton("Пара"), types.KeyboardButton("Настройка")) # add 2 buttons
 
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
    
    global group, pgroup, dist_skip
    global change_group_flag 

    try:
        if message.text[:4].lower() == 'пара': # check for command para
            change_group_flag = 0

            today = datetime.datetime.now()
            #today = today.replace(day=7, hour=8, minute=0) # DEBUG
            days_ago = 0

            user_info = trnz.read_users(message.chat.id)

            group = user_info["group"]
            pgroup = user_info["pgroup"]
            dist_skip = user_info["dist_skip"]

            if group == -1:
                bot.send_message(message.chat.id, "У вас нет группы! Напишите команду Группа", reply_markup=menu)
                return

            for i in range(5): # check the last 5 days
                if getter.get_info(group, today) == 0:
                    data = trnz.json_read(f'cache/{group}.json') # read the json

                    date_call = "%s, %s %s" % (days_list[today.weekday()], today.day, month_list[today.month - 1]) # date to format: Суббота, 7 декабря

                    para_time = today # write to para_time date

                    for i in range(len(data)):
                        dist = bool(dist_skip == '1' and data[i]['room'] == "дист")
                        if dist:
                            continue
                        
                        if_consist_pg = data[i]['subject'][len(data[i]['subject']) - 5]
                        if if_consist_pg != pgroup and (if_consist_pg == '1' or if_consist_pg == '2'):
                            continue

                        para_time = para_time.replace(hour=int(data[i]['time-start'].split(':')[0]), minute=int(data[i]['time-start'].split(':')[1])) # write to para_time starts   time

                        delta = para_time - today # calculate delta
                        para_time_30 = para_time

                        minute_buff = para_time_30.minute + 30 # calculate +30 minutes from start

                        if minute_buff <= 59: # manual convert into hours
                            para_time_30 = para_time_30.replace(minute=minute_buff)
                        else:
                            para_time_30 = para_time_30.replace(minute=(minute_buff - 60), hour=(para_time_30.hour + 1))

                        if para_time_30 > today: # check if nearest para
                            
                            if days_ago > 0: # check todsy is para
                                bot.send_message(message.chat.id, f"Ближайшая пара через: {days_ago} дн\n{date_call}\n{data[i]['number']}, {data[i]['subject']}.\nПройдёт: {data[i]['time-start']} - {data [i]['time-end']},\nПрепод: {data[i]['teacher']}\nКабинет: {data[i]['room']}", reply_markup=menu)
                            else:
                                bot.send_message(message.chat.id, f"Ближайшая пара через: {str(delta)[:5].split(':')[0]}ч {str(delta)[:5].split(':')[1]}м\n{date_call}\n{data[i]['number']}, {data[i]['subject']}.\nПройдёт: {data[i]['time-start']} - {data [i]['time-end']},\nПрепод: {data[i]['teacher']}\nКабинет: {data[i]['room']}", reply_markup=menu)
                            return
                    
                    print("im here2")
                    days_ago = days_ago + 1
                    today += datetime.timedelta(days=1)
                    today = today.replace(hour=0, minute=0)



                else: # if today is no para
                    print("im here3")
                    days_ago = days_ago + 1
                    today += datetime.timedelta(days=1)
                    today = today.replace(hour=0, minute=0)


            bot.send_message(message.chat.id, "В ближайшее время нет пар!", reply_markup=menu) # if no para in nearest 5 days

        elif message.text[:9].lower() == 'настройка': # options command
            bot.send_message(message.chat.id, "А теперь напиши свою группу!", reply_markup=menu)

            change_group_flag = 1
            
            user_info = trnz.read_users(message.chat.id)

            group = user_info["group"]
            pgroup = user_info["pgroup"]
            dist_skip = user_info["dist_skip"]


        elif change_group_flag == 1: # change group command
            group = message.text
            
            bot.send_message(message.chat.id, "Напишите вашу п/г", reply_markup=menu)
            change_group_flag = 2

        elif change_group_flag == 2:
            pgroup = message.text
            bot.send_message(message.chat.id, "Напишите, хотите ли вы пропуск дистанционных пар? (нет - 0/да - 1)", reply_markup=menu)
            change_group_flag = 3
        
        elif change_group_flag == 3:
            dist_skip = message.text

            if trnz.write_users(message.chat.id, group, pgroup, dist_skip) == -1: # try to write and check if all good
                bot.send_message(message.chat.id, "Произошла ошибка", reply_markup=menu)
                change_group_flag = 0
                return

            change_group_flag = 0
            bot.send_message(message.chat.id, "Настройка завершена!", reply_markup=menu)

        else: # if uncorrect command
            bot.send_message(message.chat.id, "некорректная команда", reply_markup=menu)
    except Exception as e:
        trnz.log_write('logs/errors.log', ("main.py: " + str(e)))

bot.infinity_polling()
