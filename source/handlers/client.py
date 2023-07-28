from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import get_inline_keyboard, get_reg_keyboard
from services import yaml_worker
from filters import button_filter
from data_base import sql_worker
from aiogram.dispatcher.filters import Text
import random
from services import MessageWorker

message_worker = MessageWorker()

#hobby_button_handler"
async def hobby_button(message : types.Message):
    message_worker.save_message(message.text)
    await bot.send_message(message.from_user.id, f"Что надо в локации {message.text}?", reply_markup = get_inline_keyboard(message.text))

#записаться
async def insert_visitor(call : types.CallbackQuery):
    if await sql_worker.is_Trusted(call.from_user.id):
        period = await sql_worker.is_final()
        if period == False:
            await sql_worker.insert_visitor(call.from_user.id, yaml_worker.get_location(call.data.split(",")[0]), "visitors", "time_interval")
            await bot.send_message(call.from_user.id, "Вы успешно записались")
        else:
            button_name = yaml_worker.get_button_name(await sql_worker.get_last_location(call.from_user.id))
            await bot.send_message(call.from_user.id, F"На данный момент вы не законили тренировку в\n{button_name}.\n\nВремя до конца: \n{period}")
    else:
        await bot.send_message(call.from_user.id, F"Либо вы заходили к нам в гости давно,\nлибо вообще не были у нас 😔.\nВ любом случае зарегестрируйтесь у администратора.\n\nДля регистрации\nнажмите на кнопку ниже\nи покажите код администратору.", reply_markup = get_reg_keyboard(message_worker.get_message()))

#регистрация
async def registration(call : types.CallbackQuery):
    code = random.randint(1000, 9999)
    
    await sql_worker.insert_visitor(call.from_user.id, yaml_worker.get_location(call.data.split(",")[0]), "visitors_waiting", "waiting_time_interval", code)
    await bot.send_message(call.from_user.id, f"Скажите или покажите этот код администратору:\n{code}")

#узнать кол-во поситителей
async def get_count_visitor(call : types.CallbackQuery):
    button_name = call.data.split(',')[0]
    await bot.send_message(call.from_user.id, f"На данный момент в {button_name}: {await sql_worker.get_amount_visitors(button_name)}")

#Информация о текущей сессии
async def get_info_session(message : types.Message):
    await bot.send_message(message.from_user.id, f"Инфо")

def register_handlers_client(dp : Dispatcher):
    dp.register_callback_query_handler(registration, lambda query: query.data.split(",")[1] == "Регистрация")
    dp.register_callback_query_handler(insert_visitor, button_filter.isInsert())
    dp.register_callback_query_handler(get_count_visitor, button_filter.isAmount())
    dp.register_message_handler(hobby_button, button_filter.isHobbyButton())
    dp.register_message_handler(get_info_session, Text(equals="инфо о текущей сессии", ignore_case=True))