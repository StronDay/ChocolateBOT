from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import get_waiting_keyboard
from keyboards import cd_accept, cd_code, cd_location
from data_base import sql_worker
from services import yaml_worker
from filters import button_filter

#Регистрация
async def registration_visitors(message : types.Message):
    await bot.send_message(message.from_user.id, f"Список пользователей на подтверждение:", reply_markup = get_waiting_keyboard())

async def insert_wiating_user(call : types.CallbackQuery, callback_data: dict):
    await sql_worker.insert_visitor(callback_data.get("id_user"), callback_data.get("location"))
    await bot.send_message(call.from_user.id, "Пользователь добавлен")
    await bot.send_message(callback_data.get("id_user"), f"Администратор вас добавил в {yaml_worker.get_button_name(callback_data.get('location'))}")

async def code_inline(call : types.CallbackQuery, callback_data: dict):
    await bot.send_message(call.from_user.id, callback_data.get("code"))

async def location_inline(call : types.CallbackQuery, callback_data: dict):
    await bot.send_message(call.from_user.id, callback_data.get("location"))

def register_handlers_client(dp : Dispatcher):
    dp.register_callback_query_handler(code_inline,  button_filter.isAdmin(), button_filter.isModer(), cd_code.filter())
    dp.register_callback_query_handler(location_inline,  button_filter.isAdmin(), button_filter.isModer(), cd_location.filter())
    dp.register_callback_query_handler(insert_wiating_user,  button_filter.isModer(), cd_accept.filter())

    dp.register_message_handler(registration_visitors, button_filter.isModer(), commands = "Зарегистрировать_пользователя")