import re

import telebot
from telebot import types

import config

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    with open('static/hi_sticker.webp', 'rb') as sticker:
        bot.send_sticker(message.chat.id, sticker)

    markup_for_time_setting = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup_for_time_setting.add('Set Time')
    bot.send_message(message.chat.id, f'Welcome {message.from_user.first_name}! '
                                      f'\nI am a <b>specific</b> alarm bot!'
                                      f'\nChoose regularity of an alarm!'
                     , parse_mode='html', reply_markup=markup_for_time_setting)


def choose_alarm():
    choice = types.InlineKeyboardMarkup(row_width=2)

    do_it_regularly = types.InlineKeyboardButton('Do it regularly', callback_data='regularly')
    ask_everyday = types.InlineKeyboardButton('Ask everyday', callback_data='ask')

    choice.add(do_it_regularly, ask_everyday)

    return choice


@bot.message_handler(content_types=['text'])
def message_repeater(message):
    if message.chat.type == 'private':
        if is_valid_time_for_alarm(message=message):
            markup_for_choice = choose_alarm()
            bot.send_message(message.chat.id, text='\tShould I', reply_markup=markup_for_choice)


def is_valid_time_for_alarm(message) -> bool:
    is_time_valid = False
    if message.text == 'Set Time':
        bot.send_message(message.chat.id, text='Set alarm time in H:MM format for example 08:12')
    elif re.match('(^([0-9]{1,2}):([0-9]{2})$)', message.text):
        time_list = message.text.split(':')
        print(time_list)
        if int(time_list[0]) < 24:
            is_time_valid = True
        else:
            bot.send_message(message.chat.id, text='I support only 24 hours format, please set correct time')
    else:
        bot.send_message(message.chat.id, text='Set correct time!')

    return is_time_valid


if __name__ == '__main__':
    # RUN
    bot.polling(none_stop=True)
