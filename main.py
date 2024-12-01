import telebot
import datetime
from telebot import types

bot = telebot.TeleBot('8130108661:AAES_8zx0x-fWAucFfUQ7GHTmFqV_WES5k4')

#calculation command body/орган управления расчетами

#end calculation command body/органа управления расчетами
menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
para_start = types.KeyboardButton("время до начала следующей пары по расписанию")
para_end = types.KeyboardButton("время до конца слеующей пары")
menu.add(para_start)

back = types.ReplyKeyboardMarkup(resize_keyboard=True)
back_button = types.KeyboardButton("аим ис кам бек кхе кхе..")
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
    start_times_pars_hours = x_start_hours
    start_times_pars_minutes = x_start_minutes
    ends_times_pars_hoirs = x_ends_hors
    ends_times_pars_minutes = x_ends_minutes
    if message.text == 'Назад':
        bot.send_message(message.chat.id, "Добро пожаловать обратно сударь каково ваше следующие желание",reply_markup=menu)
    elif message.text == 'время до начала следующей пары':
        bot.send_message(message.chat.id, f"время до начала следующей пары = {start_times_pars_hours}:{start_times_pars_minutes}", reply_markup=back)
    elif message.text == 'время до конца слеующей пары':
        bot.send_message(message.chat.id, f"время до начала следующей пары = {ends_times_pars_hoirs}:{ends_times_pars_minutes}", reply_markup=back)

bot.infinity_polling()