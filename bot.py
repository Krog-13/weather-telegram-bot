import telebot
import config
from telebot import types
import simple
import api
import check_valid
import datetime
import thisday
from datetime import timedelta
"""
Telebot shows weather in the Yaraslavl of the city 
16 days weather forecast
username is Telebot @Gashanbot
"""
#sign of "gradus"
degree_sign = chr(176)
DAY_NOW = 0
DAY_WEATHER_FORECAST = 15
bot = telebot.TeleBot('Enter your bot TOKEN')

#weather forecast
access_days = [i for i in range(16)]
today = datetime.datetime.now()
limit_days = timedelta(days=DAY_WEATHER_FORECAST)
last_data = today + limit_days

@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    sti = open('static/sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    #keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("weather today")
#    item2 = types.KeyboardButton("weather tomorrow")
    markup.add(item1,)

    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, Узнай погоду в г.Ярославль"
                     " Введите дату в цифровом формате <em>мм.дд</em> \nДоступные даты прогноза с <ins>{2}</ins> по <ins>{3}</ins> ".format(
                         message.from_user, bot.get_me(), today.date(), last_data.date()),
                     parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types = ['text'])
def main(message):
    if message.chat.type == 'private':
        if message.text == 'weather today':
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("t {}C".format(degree_sign), callback_data='temp')
            item2 = types.InlineKeyboardButton('ALL', callback_data='all')
            markup.add(item1, item2)
            bot.send_message(message.chat.id, 'Что Вас интересует?', reply_markup=markup)
            return None

        if not check_valid.check_data(message.text): #check valid foramt 00.00 only int
            bot.send_message(message.chat.id,'Пожалуйста, введите дату в цифравом формате <b>ММ.ДД</b> \nНапоминаем доступные даты с {} по {}'.format(today.date(), last_data.date()),
                             parse_mode='html')
            return None

        check_date = simple.correct_date(message.text) # checks the specified period
        if check_date in access_days:
            bot.send_message(message.chat.id, 'Метеоданные за <ins>{0[3]}</ins>:\n'
                                              ' <b>температура</b> - {0[0]}{1}C\n'
                                              ' <b>вероятность осадков</b> - {0[1]}%\n'
                                              ' <b>давление</b> - {0[4]} мм рт.ст.\n'
                                              ' <b>влажность</b> - {0[2]}%'
                             .format(api.send_weather(check_date), degree_sign), parse_mode='html')

        elif check_date not in access_days:
            bot.send_message(message.chat.id, 'К сожалению Я могу показать погоду только в период\n'
                                              'c {} по {}'.format(today.date(), last_data.date()))
        else:
            bot.send_message(message.chat.id, 'I do not understand')



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'temp':
                bot.send_message(call.message.chat.id, 'Температура воздуха {0[0]}{1}C'.format(api.send_weather(DAY_NOW),degree_sign ), parse_mode='html')
            elif call.data == 'all':
                bot.send_message(call.message.chat.id, '<ins>Метеоданные</ins>:\n'
                                              ' <b>температура</b> - {0[0]}{1}C\n'
                                              ' <b>вероятность осадков</b> - {0[1]}%\n'
                                              ' <b>давление</b> - {0[4]} мм рт.ст.\n'
                                              ' <b>влажность</b> - {0[2]}%'
                             .format(api.send_weather(DAY_NOW), degree_sign), parse_mode='html')

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Сегодня {}'.format(thisday.day_of_week),
                                  reply_markup=None)

            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Погода в Ярославле")

    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)
