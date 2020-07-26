import telebot
import config
import random
import datetime
from telebot import types
import simple
import api
import check_valid
import datetime
from datetime import timedelta
bot = telebot.TeleBot(config.TOKEN)

access_days = [i for i in range(16)]
today = datetime.datetime.now()
limit_days = timedelta(days=15)
last_data = today + limit_days
@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    sti = open('static/sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    #keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("weather today")
    item2 = types.KeyboardButton("weather tomorrow")
    markup.add(item1, item2)

    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, Узнай погоду в г.Ярославль"
                     " Введите дату в формате <em>мм.дд</em> \nДоступные даты прогноза с <ins>{2}</ins> по <ins>{3}</ins> ".format(
                         message.from_user, bot.get_me(), today.date(), last_data.date()),
                     parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types = ['text'])
def main(message):
    if message.chat.type == 'private':
        if not check_valid.check_data(message.text):
            bot.send_message(message.chat.id,'Пожалуйста, введите дату в цифравом формате <em>мм.дд</em> \nНапоминаем доступные даты с {} по {}'.format(today.date(), last_data.date()),
                             parse_mode='html')
            return None
        check_date = simple.correct_date(message.text)
        if check_date in access_days:
            #day = simple.correct_date(message.text)
            bot.send_message(message.chat.id, 'В городе {0[0]} градусов\nДата прогноза - {0[1]} '.format(api.send_weather(check_date)))
        elif check_date not in access_days:
            bot.send_message(message.chat.id, 'К сожалению Я могу показать погоду только в период\n'
                                              'c {} по {}'.format(today.date(), last_data.date()))
        elif message.text == 'weather tomorrow':
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("morning", callback_data='good')
            item2 = types.InlineKeyboardButton('night', callback_data='BAD')
            markup.add(item1, item2)
            bot.send_message(message.chat.id, 'select half a day', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'I do not understand')



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, '24 degree')
            elif call.data == 'BAD':
                bot.send_message(call.message.chat.id, '18 degree')

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="***",
                                  reply_markup=None)

            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Погода в городе")

    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)

