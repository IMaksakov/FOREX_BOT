import telebot
from telebot import types
import requests
import json
from configs import *
from extensions import APIException, Converter


bot = telebot.TeleBot(TOKEN)

#приветствие
@bot.message_handler(commands= ["start", "help"])
def greetings (message: telebot.types.Message):
    test = "Привет!"
    bot.send_message(message.chat.id, text)

#список валют
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Я умею конвертировать:"
    for key in exchanges.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)
    
#отлавливание ошибок
@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Некорректный ввод - пересмотри число переменных)')
        answer = Converter.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде. \n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка. \n{e}")
    else:
        bot.reply_to(message, answer)

bot.polling()