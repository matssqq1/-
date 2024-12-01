import telebot
from telebot import types

bot = telebot.TeleBot('8130108661:AAES_8zx0x-fWAucFfUQ7GHTmFqV_WES5k4')

@bot.message_handler(commands=['start'])
def start_meassage(message):
    bot.send_message(message.chat.id, "Hellol!")

bot.infinity_polling()