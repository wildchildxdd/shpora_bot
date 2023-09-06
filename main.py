import telebot
import sqlite3
import os
import config
import texts
from telebot import types
import utils
from db import DB
import time
import texts

db = DB()

# Инициализация бота с помощью API токена
bot = telebot.TeleBot(config.CREDS)

# Определение состояний для ConversationHandler
GET_WEAR_DEVICE_MODEL, GET_STORAGE_CAPACITY = range(2)

# Создаем клавиатуру с кнопками
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item_calibrate = types.KeyboardButton("Калибровать")
item_begin = types.KeyboardButton("Начать")

markup.add(item_calibrate, item_begin)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_data = {}
    user_data['telegram_id'] = user_id

    bot.send_message(message.chat.id, texts.INIT_MESSAGE, reply_markup=markup)
    
    bot.register_next_step_handler(message, calibrate, user_data)

def calibrate(message, user_data):
    user_id = user_data['telegram_id']
    symbol_capacity = int(message.text)
    parts = utils.get_parts(symbol_capacity, texts.TEST_TEXT)
    bot.send_message(message.chat.id, "Пожалуйста, сверните телеграм и заблокируйте экран. Через 5 секунд придут уведомления")
    time.sleep(5)
    for part in parts:
        time.sleep(0.5)
        bot.send_message(message.chat.id, part, reply_markup=markup)
    db.set_symbol_capacity(symbol_capacity, user_id)

@bot.message_handler(func=lambda message: message.text == "Калибровать")
def retry_over_button_click(message):
    user_id = message.from_user.id
    user_data = {}
    user_data['telegram_id'] = user_id

    bot.send_message(message.chat.id, "Пожалуйста, введите количество символов", reply_markup=markup)
    bot.register_next_step_handler(message, calibrate, user_data)

@bot.message_handler(func=lambda message: message.text == "Начать")
def create_cheat(message):
    user_id = message.from_user.id
    user_data = {}
    user_data['telegram_id'] = user_id
    bot.send_message(message.chat.id, "Скопируйте и вставьте текст шпаргалки")
    bot.register_next_step_handler(message, cheat, user_data)

def cheat(message, user_data):
    user_id = user_data['telegram_id']
    text = message.text
    symbol_capacity = db.get_symbol_capacity(user_id)
    parts = utils.get_parts(symbol_capacity, text)
    bot.send_message(message.chat.id, "Пожалуйста, сверните телеграм и заблокируйте экран. Через 5 секунд придут уведомления")
    time.sleep(5)

    for part in parts:
        time.sleep(0.5)
        bot.send_message(message.chat.id, part, reply_markup=markup)

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)
