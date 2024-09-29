import telebot
import requests
import config as config

from telebot import types


bot = telebot.TeleBot(config.API_TOKEN)
user_names = {}


def get_name(message):
    user_names[message.chat.id] = message.text
    send_usd_rate(message)


def send_usd_rate(message):
    data = requests.get(config.URL).json()
    usd_rate = data['Valute']['USD']['Value']

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Обновить курс')
    markup.add(itembtn1)
    bot.send_message(message.chat.id, text=f'Рад знакомству, {user_names[message.chat.id]}! Курс доллара сегодня {usd_rate} рублей', reply_markup=markup)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.id not in user_names:
        bot.send_message(message.chat.id, "Как вас зовут?")
        bot.register_next_step_handler(message, get_name)
    else:
        send_usd_rate(message)


@bot.message_handler(func=lambda message: message.text == 'Обновить курс')
def update_usd_rate(message):
    send_usd_rate(message)


bot.polling(none_stop=True)
