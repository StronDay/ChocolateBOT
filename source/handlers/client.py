from aiogram import types, Dispatcher
from filters import button_filter
from create_bot import bot
from data_base import sql_worker
from keyboards import get_inline_keyboard, get_reg_keyboard, training_choise_keyboard, time_keyboard
from keyboards import cd_time, cd_registration, cd_amount_vis, cd_insert_vis
from services import yaml_worker
from services import get_text
from services import MessageWorker
from aiogram.dispatcher.filters import Text
import random
from aiogram.dispatcher.filters.state import State, StatesGroup

message_worker = MessageWorker()

class FSMClient(StatesGroup):
    time = State()

#hobby_button_handler"
async def hobby_button(message : types.Message):
    message_worker.save_message(message.text)
    await bot.send_message(message.from_user.id, get_text("location_text").format(message.text), reply_markup = get_inline_keyboard(message.text))

#записаться
async def insert_visitor(call : types.CallbackQuery, callback_data: dict):
    if await sql_worker.is_Trusted(call.from_user.id):
        period = await sql_worker.is_final(call.from_user.id)
        if period == False:
            await sql_worker.insert_visitor(call.from_user.id, yaml_worker.get_location(callback_data.get("button")))
            await bot.send_message(call.from_user.id, get_text("successfully_signed_text"))
        else:
            button_name = yaml_worker.get_button_name(await sql_worker.get_last_location(call.from_user.id))
            await bot.send_message(call.from_user.id, get_text("no_finish_text").format(button_name, period), reply_markup = training_choise_keyboard)
    else:
        await bot.send_message(call.from_user.id, get_text("no_trust_text"), reply_markup = get_reg_keyboard(message_worker.get_message()))

#регистрация
async def registration(call : types.CallbackQuery, callback_data: dict):
    code = random.randint(1000, 9999)
    
    await sql_worker.insert_waiting(call.from_user.id, yaml_worker.get_location(callback_data.get("button")), code)
    await bot.send_message(call.from_user.id, get_text("code_text").format(code))

#узнать кол-во поситителей
async def get_count_visitor(call : types.CallbackQuery, callback_data: dict):
    button_name = callback_data.get("button")
    await bot.send_message(call.from_user.id, get_text("amount_visitors_text").format(button_name, await sql_worker.get_amount_visitors(button_name)))

#Информация о текущей сессии
async def get_info_session(message : types.Message):
    period = await sql_worker.is_final(message.from_user.id)

    if period == False:
        await bot.send_message(message.from_user.id, get_text("no_traning_text"))
    else:
        button_name = yaml_worker.get_button_name(await sql_worker.get_last_location(message.from_user.id))
        await bot.send_message(message.from_user.id, get_text("yes_tranning_text").format(button_name, period), reply_markup = training_choise_keyboard)

#Завершить сессию
async def complete_traning(call : types.CallbackQuery):
    period = await sql_worker.is_final(call.from_user.id)
    if period == False:
        await bot.send_message(call.from_user.id, get_text("complete_traning_text"))
    else:
        await sql_worker.complete_time(call.from_user.id)
        await bot.send_message(call.from_user.id, get_text("no_complete_traning_text"))

#Продлить сессию 1
async def extend_tranning(call : types.CallbackQuery):
    await FSMClient.time.set()
    await bot.send_message(call.from_user.id, get_text("choice_time"), reply_markup = time_keyboard)

#Продлить сессию 2
async def extend_tranning_time(call : types.CallbackQuery,  callback_data: dict, state : FSMClient):
    async with state.proxy() as data:
        data["time"] = callback_data.get("time")

    await sql_worker.extend_time(call.from_user.id, data["time"])

    await bot.send_message(call.from_user.id, get_text("time_extended"))
    await state.finish()

def register_handlers_client(dp : Dispatcher):
    dp.register_callback_query_handler(extend_tranning, lambda query: query.data == "Продлить", state=None)
    dp.register_callback_query_handler(complete_traning, lambda query: query.data == "Завершить")
    dp.register_callback_query_handler(extend_tranning_time, cd_time.filter(), state=FSMClient.time)
    dp.register_callback_query_handler(registration, cd_registration.filter())
    dp.register_callback_query_handler(insert_visitor, cd_insert_vis.filter())
    dp.register_callback_query_handler(get_count_visitor, cd_amount_vis.filter())
    dp.register_message_handler(hobby_button, button_filter.isHobbyButton())
    dp.register_message_handler(get_info_session, Text(equals="узнать о текущей тренировке", ignore_case=True))