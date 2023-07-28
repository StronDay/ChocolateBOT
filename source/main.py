# import telebot
# from telebot import types

# from datetime import datetime
# import random
# from data_base_worker import DataBaseWorker
#import buttons

######################################################################################
#try:
#    connection = psycopg2.connect(
#        host = host,
#        user = user,
#        password = password,
#        database = db_name
#    )
#
#    connection.autocommit = True
#
#    with connection.cursor() as cursor:
#        cursor.execute('SELECT version();')
#
#        print(f'Server version: {cursor.fetchone()}')
#
#except Exception as _ex:
#    print('[INFO] Error while working with PostgreSQL ', _ex)
#finally:
#    if connection:
#        connection.close()
#        print('[INFO] PostgreSQL connection closed')
#
######################################################################################

# data_base = DataBaseWorker()

# bot = telebot.TeleBot('nety tokena tyt k sojaleniy :(((( ))))');

# class buttons:

#     gym_button_text = '💪🏻 Зал'
#     yoga_button_text = '🧘🏻 Йога'
#     karate_button_text = '🥋 Карате'
#     pool_button_text = '🏊🏼 Бассейн'

# @bot.message_handler(commands=['start'])
# def start(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard = True)

#     gym_button = types.KeyboardButton(buttons.gym_button_text)
#     yoga_button = types.KeyboardButton(buttons.yoga_button_text)
#     karate_button = types.KeyboardButton(buttons.karate_button_text)
#     pool_button = types.KeyboardButton(buttons.pool_button_text)

#     markup.row(gym_button, yoga_button)
#     markup.row(karate_button, pool_button)

#     bot.send_message(message.chat.id, 'Привет', reply_markup=markup)
#     #bot.register_next_step_handler(message, on_click)

# @bot.callback_query_handler(func = lambda callback: True)
# def callback_message(callback):

#     match callback.data:
#         case 'вы успешно записались в зал':

#             id_user = random.randint(1, 9999)

#             data_base.insert_visitor(callback.message.chat.id, 'gym')
#             bot.send_message(callback.message.chat.id, callback.data)
#         case 'вы успешно записались на йогу':

#             id_user = random.randint(1, 9999)

#             data_base.insert_visitor(callback.message.chat.id, 'yoga')
#             bot.send_message(callback.message.chat.id, callback.data)
#         case 'вы успешно записались на карате':

#             id_user = random.randint(1, 9999)

#             data_base.insert_visitor(callback.message.chat.id, 'karate')
#             bot.send_message(callback.message.chat.id, callback.data)
#         case 'вы успешно записались в бассейн':

#             id_user = random.randint(1, 9999)

#             data_base.insert_visitor(callback.message.chat.id, 'pool')
#             bot.send_message(callback.message.chat.id, callback.data)
#         case "В зале сейчас ":
#             bot.send_message(callback.message.chat.id, f"В зале сейчас {data_base.get_amount_visitors('gym')}")
#         case "На йоге сейчас ":
#             bot.send_message(callback.message.chat.id, f"На йоге сейчас {data_base.get_amount_visitors('yoga')}")
#         case "На карате сейчас ":
#             bot.send_message(callback.message.chat.id, f"На карате сейчас {data_base.get_amount_visitors('karate')}")
#         case "В бассейне сейчас ":
#             bot.send_message(callback.message.chat.id, f"В бассейне сейчас {data_base.get_amount_visitors('pool')}")



# @bot.message_handler(content_types='text')
# def answer(message):

#     markup = types.InlineKeyboardMarkup()

#     visitors_number = types.InlineKeyboardButton('Узнать кол-во поситителей', callback_data = 'Узнать кол-во поситителей')

#     match message.text:
#         case buttons.gym_button_text:

#             sign_up = types.InlineKeyboardButton('Записаться', callback_data = 'вы успешно записались в зал')
#             visitors_number = types.InlineKeyboardButton('Узнать кол-во поситителей', callback_data = 'В зале сейчас ')

#             markup.row(sign_up)
#             markup.row(visitors_number)

#             bot.send_message(message.chat.id, 'Что вы хотели бы сделать в зале', reply_markup = markup)
#         case buttons.yoga_button_text:

#             sign_up = types.InlineKeyboardButton('Записаться', callback_data = 'вы успешно записались на йогу')
#             visitors_number = types.InlineKeyboardButton('Узнать кол-во поситителей', callback_data = 'На йоге сейчас ')

#             markup.row(sign_up)
#             markup.row(visitors_number)

#             bot.send_message(message.chat.id, 'Что вы хотели бы сделать на йоге', reply_markup = markup)
#         case buttons.karate_button_text:

#             sign_up = types.InlineKeyboardButton('Записаться', callback_data = 'вы успешно записались на карате')
#             visitors_number = types.InlineKeyboardButton('Узнать кол-во поситителей', callback_data = 'На карате сейчас ')

#             markup.row(sign_up)
#             markup.row(visitors_number)

#             bot.send_message(message.chat.id, 'Что вы хотели бы сделать на карате', reply_markup = markup)
#         case buttons.pool_button_text:

#             sign_up = types.InlineKeyboardButton('Записаться', callback_data = 'вы успешно записались в бассейн')
#             visitors_number = types.InlineKeyboardButton('Узнать кол-во поситителей', callback_data = 'В бассейне сейчас ')

#             markup.row(sign_up)
#             markup.row(visitors_number)

#             bot.send_message(message.chat.id, 'Что вы хотели бы сделать в бассейне', reply_markup = markup)



# bot.polling(non_stop=True)
# data_base.close_data_base()
##########################################################################################

from aiogram.utils import executor
from create_bot import dp
from handlers import client, admin, general, moderator
from data_base import sql_worker

async def on_startup(_):
    print("Бот вышел в онлайн")

sql_worker.sql_start()


general.register_handlers_client(dp)
admin.register_handlers_client(dp)
client.register_handlers_client(dp)
moderator.register_handlers_client(dp)

executor.start_polling(dp, skip_updates = True, on_startup = on_startup)
sql_worker.sql_close()