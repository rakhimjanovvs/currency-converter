import requests
import telebot
import config

link = 'https://cbu.uz/ru/arkhiv-kursov-valyut/json/'
rate_usd = float(requests.get(link).json()[0]['Rate'])
rate_eur = float(requests.get(link).json()[1]['Rate'])
rate_rub = float(requests.get(link).json()[2]['Rate'])

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Введите сумму в сумах!')
    bot.register_next_step_handler(message, converter)

@bot.message_handler(content_types=['text'])
def text_msg(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Введите сумму в сумах!')
    bot.register_next_step_handler(message, converter)

def converter(message):
    user_id = message.from_user.id
    num = int(message.text)
    usd = num / rate_usd
    eur = num / rate_eur
    rub = num / rate_rub
    bot.send_message(user_id, f'USD: {usd:.2f} \nEUR: {eur:.2f} \nRUB: {rub:.2f}')
    bot.send_message(user_id, 'Введите сумму в сумах!')
    bot.register_next_step_handler(message, converter)

# Запуск бота
bot.polling(non_stop=True)