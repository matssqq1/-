import telebot
import datetime
from telebot import types

bot = telebot.TeleBot('8130108661:AAES_8zx0x-fWAucFfUQ7GHTmFqV_WES5k4')
#calculation command body/орган управления расчетами
now = datetime.datetime.now()
minutes_now = now.minute
hours_now = now.hour
if hours_now == 
times = 10
#end calculation command body/органа управления расчетами
menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
para_start = types.KeyboardButton("время до начала следующей пары")
para_end = types.KeyboardButton("время до конца слеующей пары")
menu.add(para_start)

back = types.ReplyKeyboardMarkup(resize_keyboard=True)
back_button = types.KeyboardButton("Назад")
back.add(back_button)

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
    start_times_pars = times
    ends_times_pars = times
    if message.text == 'Назад':
        bot.send_message(message.chat.id, "Добро пожаловать обратно сударь каково ваше следующие желание",reply_markup=menu)
    elif message.text == 'время до начала следующей пары':
        bot.send_message(message.chat.id, f"время до начала следующей пары = {start_times_pars}минут", reply_markup=back)
    elif message.text == 'время до конца слеующей пары':
        bot.send_message(message.chat.id, f"время до начала следующей пары = {ends_times_pars}минут", reply_markup=back)

bot.infinity_polling()