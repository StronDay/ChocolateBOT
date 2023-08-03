from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot
from keyboards import get_waiting_keyboard
from keyboards import get_buttons
from keyboards import cd_accept, cd_code, cd_location, cd_button_action
from data_base import sql_worker
from services import yaml_worker
from filters import button_filter

class FSMModer(StatesGroup):
    location = State()

#Регистрация
async def registration_visitors(message : types.Message):
    await bot.send_message(message.from_user.id, f"Список пользователей на подтверждение:", reply_markup = await get_waiting_keyboard())

#Добавить пользователя(бабулю), который не хочет или не может проходить регистрацию 1
async def add_granny(message : types.Message):
    await FSMModer.location.set()
    await bot.send_message(message.from_user.id, f"Список пользователей на подтверждение:", reply_markup = get_buttons("add granny"))

#Добавить пользователя(бабулю), который не хочет или не может проходить регистрацию 2
async def add_granny_choise_location(call : types.CallbackQuery, callback_data: dict, state : FSMModer):
    async with state.proxy() as data:
        data["location"] = yaml_worker.get_location(callback_data.get("button"))

    await sql_worker.insert_visitor("777", data["location"])
    await bot.send_message(call.from_user.id, "Бабуля была добавлена")
    await state.finish()

async def insert_wiating_user(call : types.CallbackQuery, callback_data: dict):
    if await sql_worker.is_final(call.from_user.id) == False:
        await sql_worker.insert_visitor(callback_data.get("id_user"), callback_data.get("location"))
        await bot.send_message(call.from_user.id, "Пользователь добавлен")
        await bot.send_message(callback_data.get("id_user"), f"Администратор вас добавил в {yaml_worker.get_button_name(callback_data.get('location'))}")
    else:
        await bot.send_message(call.from_user.id, "Пользователь уже был добавлен")

async def code_inline(call : types.CallbackQuery, callback_data: dict):
    await bot.send_message(call.from_user.id, callback_data.get("code"))

async def location_inline(call : types.CallbackQuery, callback_data: dict):
    await bot.send_message(call.from_user.id, callback_data.get("location"))

def register_handlers_client(dp : Dispatcher):
    dp.register_callback_query_handler(code_inline, button_filter.isModer(), cd_code.filter())
    dp.register_callback_query_handler(location_inline, button_filter.isModer(), cd_location.filter())
    dp.register_callback_query_handler(insert_wiating_user,  button_filter.isModer(), cd_accept.filter())

    dp.register_message_handler(registration_visitors, button_filter.isModer(), commands = "Зарегистрировать_пользователя")
    dp.register_message_handler(add_granny, button_filter.isModer(), commands = "Добавить_бабулю", state=None)
    dp.register_callback_query_handler(add_granny_choise_location, button_filter.isModer(), cd_button_action.filter(action = "add granny"), state = FSMModer.location)