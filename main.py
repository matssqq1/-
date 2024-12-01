import telebot
from telebot import types
from src.test import taims

#вытаскиваем из масива часы и менуты для бота
a = taims()
start_hous = a[0]
start_minets = a[1]
ends_hous = a[2]
ends_minets = a[3]

bot = telebot.TeleBot('8130108661:AAES_8zx0x-fWAucFfUQ7GHTmFqV_WES5k4')

#end calculation command body/органа управления расчетами
menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
para_ends = types.KeyboardButton("Время до каонца текущей пары")
para_start = types.KeyboardButton("время до начала следующей пары по расписанию и конца текущий")
menu.add(para_start,para_ends)

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
    start_hous_bot = start_hous
    start_minets_bot = start_minets
    ends_hous_bot = ends_hous
    ends_minets_bot = ends_minets
    if message.text == 'аим ис кам бек кхе кхе..':
        bot.send_message(message.chat.id, "Добро пожаловать обратно сударь каково ваше следующие желание", reply_markup=menu)
    elif message.text == 'время до начала следующей пары по расписанию и конца текущий':
        bot.send_message(message.chat.id, f"{start_hous_bot}:{start_minets_bot}", reply_markup=back)
    elif message.text == 'Время до каонца текущей пары':
        bot.send_message(message.chat.id, f"{ends_hous_bot}:{ends_minets_bot}", reply_markup=back)
bot.infinity_polling()