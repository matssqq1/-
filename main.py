import telebot
from telebot import types

bot = telebot.TeleBot('8130108661:AAES_8zx0x-fWAucFfUQ7GHTmFqV_WES5k4')
#начало
#создаём калву с кнопками
menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
services = types.KeyboardButton("Services")
menu.add(services)
#создаем кнопку назад
back = types.ReplyKeyboardMarkup(resize_keyboard=True)
back_button = types.KeyboardButton("Back")
back.add(back_button)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "hellos!", reply_markup = menu)

bot.infinity_polling() #конец бота