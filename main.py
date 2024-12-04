import telebot
from telebot import types
# from src.test import taims
from api.parcer import parcer
import src.tranzactions as trnz
import datetime
# import json

# dates and months for printing data
month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
days_list = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
global group, pgroup, dist_skip
change_group_flag = 0

#вытаскиваем из масива часы и менуты для бота
# a = taims()
# start_hous = a[0]
# start_minets = a[1]
# ends_hous = a[2]
# ends_minets = a[3]

bot = telebot.TeleBot('8130108661:AAES_8zx0x-fWAucFfUQ7GHTmFqV_WES5k4')

#end calculation command body/органа управления расчетами

#para_ends = types.KeyboardButton("Время до каонца текущей пары")
#para_start = types.KeyboardButton("время до начала следующей пары")

menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(types.KeyboardButton("Пара"), types.KeyboardButton("Настройка")) # add 2 buttons
 
# back = types.ReplyKeyboardMarkup(resize_keyboard=True)
# back_button = types.KeyboardButton("аим ис кам бек кхе кхе..")
# back.add(back_button)

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
    
    try:
        if message.text[:4].lower() == 'пара': # check for command пара # flag init
            change_group_flag = 0

            today = datetime.datetime.now()
            today = today.replace(day=1, hour=14, minute=30) # DEBUG
            days_ago = 0

            group = trnz.read_users(message.chat.id)
            if group == -1:
                bot.send_message(message.chat.id, "У вас нет группы! Напишите команду Группа", reply_markup=menu)
                return

            for i in range(5): # check the last 5 days
                if getter.get_info(group, today) == 0:
                    #print("im not here")
                    data = trnz.json_read(f'cache/{group}.json') # read the json

                    date_call = "%s, %s %s" % (days_list[today.weekday()], today.day, month_list[today.month - 1]) # date to format: Суббота, 7 декабря

                    para_time = today # write to para_time date

                    for i in range(len(data)):
                        #print(str(i), str(len(data)))
                        #print(data[i])

                        para_time = para_time.replace(hour=int(data[i]['time-start'].split(':')[0]), minute=int(data[i]['time-start'].split(':')[1])) # write to para_time starts   time

                        delta = para_time - today # calculate delta
                        #print(para_time.hour, para_time.minute)
                        para_time_30 = para_time
                        para_time_30 = para_time_30.replace(minute=para_time_30.minute + 30)
                        #print(para_time_30.hour, para_time_30.minute)

                        if para_time_30 > today: # check if nearest para
                            if days_ago > 0: # check todsy is para
                                bot.send_message(message.chat.id, f"Ближайшая пара через: {days_ago} дн\n{date_call}\n{data[i]['number']}, {data[i]['subject']}.\nПройдёт: {data[i]['time-start']} - {data [i]['time-end']},\nПрепод: {data[i]['teacher']}\nКабинет: {data[i]['room']}", reply_markup=menu)
                            else:
                                bot.send_message(message.chat.id, f"Ближайшая пара через: {str(delta)[:5].split(':')[0]}ч {str(delta)[:5].split(':')[1]}м\n{date_call}\n{data[i]['number']}, {data[i]['subject']}.\nПройдёт: {data[i]['time-start']} - {data [i]['time-end']},\nПрепод: {data[i]['teacher']}\nКабинет: {data[i]['room']}", reply_markup=menu)
                            return
                        
                    days_ago = days_ago + 1
                    today += datetime.timedelta(days=1)
                    today = today.replace(hour=0, minute=0)
                    #print("im here!")


                else: # if today is no para
                    days_ago = days_ago + 1
                    today += datetime.timedelta(days=1)
                    today = today.replace(hour=0, minute=0)
                    #print("im here!")

            bot.send_message(message.chat.id, "В ближайшее время нет пар!", reply_markup=menu) # if no para in nearest 5 days

        elif message.text[:9].lower() == 'настройка': # группа command
            bot.send_message(message.chat.id, "А теперь напиши свою группу!", reply_markup=menu)

            change_group_flag = 1


        elif change_group_flag == 1: # change group command
            group = message.text
            
            bot.send_message(message.chat.id, "Напишите вашу п/г", reply_markup=menu)
            #bot.send_message(message.chat.id, "Группа сохранена", reply_markup=menu)
            #global change_group_flag
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


        # elif message.text == 'аим ис кам бек кхе кхе..':
        #     bot.send_message(message.chat.id, "Добро пожаловать обратно сударь каково ваше следующие желание", reply_markup=menu)
        # elif message.text == 'время до начала следующей пары':
        #     bot.send_message(message.chat.id, f"{start_hous_bot}:{start_minets_bot}", reply_markup=back)
        # elif message.text == 'Время до каонца текущей пары':
        #     bot.send_message(message.chat.id, f"{ends_hous_bot}:{ends_minets_bot}", reply_markup=back)
        else: # if uncorrect command
            bot.send_message(message.chat.id, "некорректная команда", reply_markup=menu)
    except Exception as e:
        trnz.log_write('logs/errors.log', ("main.py: " + str(e)))

bot.infinity_polling()
