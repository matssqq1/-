import telebot
from telebot import types

bot = telebot.TeleBot('8130108661:AAES_8zx0x-fWAucFfUQ7GHTmFqV_WES5k4')
#calculation command body/орган управления расчетами
times = "10:00"

menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
para_start = types.KeyboardButton("время до начала следующей пары")
para_end = types.KeyboardButton("время до конца слеующей пары")
menu.add(para_start, para_end)

back = types.ReplyKeyboardMarkup(resize_keyboard=True)
back_button = types.KeyboardButton("Назад")
back.add(back_button)

#start bot codding commands /start

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "hello!", reply_markup = menu)

#stop bot codding commands /stop (verigud is not deleted)

@bot.message_handler(commands=['stop'])
def message(message):
    bot.send_message(message.chat.id, "stop bots")
    bot.stop_polling()

@bot.message_handler(content_types=['text'])
def text_messages(message):
    if message.text == 'Назад':
        bot.send_message(message.chat.id, "Добро пожаловать обратно сударь",reply_markup=back)
    elif message.text == 'время до начала следующей пары':
        bot.send_message(message.chat.id, "время до следующей пары = ", times, reply_markup=back)
        
bot.infinity_polling()