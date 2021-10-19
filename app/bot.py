import os
import os.path
import string
import requests
import telebot
from telebot import types
from config import TelegramBotConfig, ParserConfig, SaveConfig
from app.web_parser import Parser
import pyshorteners
from datetime import datetime
from random import choices


s = pyshorteners.Shortener()
parser = Parser()

button_timetable_text = 'Выбрать расписание'
bot = telebot.TeleBot(TelegramBotConfig.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) # Main Keyboard-menu
    button_timetable = types.KeyboardButton(button_timetable_text)
    markup.add(button_timetable)
    bot.send_message(message.chat.id, 'Привет! Это бот-расписание УрГУПС', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def main(message):
    if message.text == button_timetable_text:
        bot.send_message(chat_id=message.chat.id, text='Пожалуйста, подождите')
        markup = get_timetable_list_buttons(ParserConfig.URL)
        bot.send_message(message.chat.id, 'Хорошо, посмотрим расписание. Нажми на кнопку для выбора', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_dict(call):
    bot.send_message(chat_id=call.message.chat.id, text='Пожалуйста, подождите')
    if call.message:
        lst = call.data.split()
        dict = {}
        dict['data_type'] = lst[0]
        if dict['data_type'] == 'parser_data':
            dict['link'] = lst[1]
            dict['format'] = lst[2]
            if dict['format'] in ParserConfig.FILE_FORMATS:
                r = requests.get(dict['link'], allow_redirects=True)
                file_name = str(int(datetime.now().timestamp())).join(choices(string.ascii_lowercase, k=4)) + dict['format']
                full_path = os.path.join(SaveConfig.SAVE_PATH, file_name)
                if not os.path.exists(SaveConfig.SAVE_PATH):
                    os.mkdir(os.path.join(SaveConfig.SAVE_PATH))
                open(full_path, 'wb').write(r.content)
                with open(full_path, "rb") as misc:
                    f = misc.read()
                bot.send_document(call.message.chat.id, f, visible_file_name='Расписание' + dict['format'])
                os.remove(full_path)
                main(message=call.message)
            if dict['format'] == 'directory':
                markup = get_timetable_list_buttons(dict['link'])
                bot.send_message(call.message.chat.id, 'Хорошо. Выбери дальше:', reply_markup=markup)


def get_timetable_list_buttons(url):
    dict = parser.get_content(url)
    markup = types.InlineKeyboardMarkup(row_width=2)
    for i in range(int(len(dict))):
        timetable_markup_keyboard_button = types.InlineKeyboardButton(
            dict[i]['name'], callback_data='parser_data' + ' ' + s.tinyurl.short(dict[i]['link']) + ' ' + dict[i]['format'])
        markup.add(timetable_markup_keyboard_button)
    return markup
