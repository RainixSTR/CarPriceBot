import telebot
from telebot import types
from config import BOT_TOKEN

import re
import datetime
from model import predict_car_price

bot = telebot.TeleBot(BOT_TOKEN)
CUR_STATE = 0


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Начнем")
    markup.add(btn1)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! "
                                           "Я помогу определить цену твоей машины. "
                                           "Для начала работы нажми кнопку \"Начать\""
                     .format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    global price, kms, fuel, seller, mode, age
    global CUR_STATE

    if message.text == "Отмена":
        CUR_STATE = 0

    if message.text == "Начнем":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Отмена")
        markup.add(btn1)
        bot.send_message(message.chat.id, text="Введите цену покупки авто в формате \"xxx.x\"".format(message.from_user), reply_markup=markup)
        CUR_STATE = 1

    elif CUR_STATE == 1:

        if re.match(r"^\d+\.\d+$", message.text):
            CUR_STATE = 2
            price = message.text
        else:
            bot.send_message(message.chat.id, text="Данные введены некорректно. "
                                                   "Введите цену покупки авто в формате \"xxx.x\"")

    if CUR_STATE == 2:
        bot.send_message(message.chat.id, text="Введите километраж в формате \"xxx.x\")")
        CUR_STATE = 3

    elif CUR_STATE == 3:
        if re.match(r"^\d+\.\d+$", message.text):
            CUR_STATE = 4
            kms = message.text
        else:
            bot.send_message(message.chat.id, text="Данные введены некорректно. "
                                                   "Введите километраж в формате \"xxx.x\"")

    if CUR_STATE == 4:

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Diesel")
        btn2 = types.KeyboardButton("CNG")
        btn3 = types.KeyboardButton("Petrol")
        btn4 = types.KeyboardButton("Отмена")
        markup.add(btn1, btn2, btn3, btn4)

        bot.send_message(message.chat.id, text="Выберите тип топлива".format(message.from_user), reply_markup=markup)
        CUR_STATE = 5

    elif CUR_STATE == 5:
        if message.text in (["Diesel", "CNG", "Petrol"]):
            CUR_STATE = 6
            fuel = 2 if message.text == 'CNG' else 1 if message.text == 'Diesel' else 0
        else:
            bot.send_message(message.chat.id, text="Данные введены некорректно. "
                                                   "Выберите тип топлива из списка ниже")

    if CUR_STATE == 6:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Dealer")
        btn2 = types.KeyboardButton("Individual")
        btn3 = types.KeyboardButton("Отмена")
        markup.add(btn1, btn2, btn3)

        bot.send_message(message.chat.id, text="Выберите тип продавца".format(message.from_user), reply_markup=markup)
        CUR_STATE = 7

    elif CUR_STATE == 7:
        if message.text in (["Dealer", "Individual"]):
            CUR_STATE = 8
            seller = 0 if message.text == 'Dealer' else 1
        else:
            bot.send_message(message.chat.id, text="Данные введены некорректно. "
                                                   "Выберите тип продавца из списка ниже")

    if CUR_STATE == 8:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Manual")
        btn2 = types.KeyboardButton("Automatic")
        btn3 = types.KeyboardButton("Отмена")
        markup.add(btn1, btn2, btn3)

        bot.send_message(message.chat.id, text="Выберите тип КП".format(message.from_user), reply_markup=markup)
        CUR_STATE = 9

    elif CUR_STATE == 9:
        if message.text in (["Manual", "Automatic"]):
            CUR_STATE = 10
            mode = 0 if message.text == 'Manual' else 1
        else:
            bot.send_message(message.chat.id, text="Данные введены некорректно. "
                                                   "Выберите тип КП из списка ниже")

    if CUR_STATE == 10:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Отмена")
        markup.add(btn1)
        bot.send_message(message.chat.id, text="Введите год покупки авто".format(message.from_user), reply_markup=markup)
        CUR_STATE = 11

    elif CUR_STATE == 11:
        if re.match(r'^\d+$', message.text):
            CUR_STATE = 12
            current_year = datetime.datetime.now().year
            age = current_year - int(message.text)
        else:
            bot.send_message(message.chat.id, text="Данные введены некорректно. "
                                                   "Введите год покупки авто")

    if CUR_STATE == 12:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Начнем")
        markup.add(btn1)
        price = predict_car_price([float(price), float(kms), fuel, seller, mode, age])
        bot.send_message(message.chat.id, text="Цена машины: {price}".format(price=float(price).__round__(3))
                         .format(message.from_user), reply_markup=markup)
        CUR_STATE = 0

    elif CUR_STATE == 0:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Начнем")
        markup.add(btn1)
        bot.send_message(message.chat.id, text="Для начала работы нажми кнопку \"Начнем\""
                         .format(message.from_user), reply_markup=markup)


bot.polling(none_stop=True)
