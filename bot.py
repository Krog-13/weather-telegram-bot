import telebot
import config
import random
import datetime
from telebot import types
import simple
import api
import check_valid
bot = telebot.TeleBot(config.TOKEN)

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
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, введите дату на ближайшие 15 дней.".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types = ['text'])
def main(message):
    if message.chat.type == 'private':
        if not check_valid.check_data(message.text):
            bot.send_message(message.chat.id,'Введите кооретную дату')
            return None

        if simple.correct_date(message.text):
            day = simple.correct_date(message.text)
            bot.send_message(message.chat.id, 'В городе {0[0]} градусов\nДата прогноза - {0[1]} '.format(api.send_weather(day)))

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

