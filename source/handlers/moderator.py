from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import get_waiting_keyboard
from data_base import sql_worker
from services import yaml_worker
from filters import button_filter

#Регистрация
async def registration_visitors(message : types.Message):
    await bot.send_message(message.from_user.id, f"Список пользователей на подтверждение:", reply_markup = get_waiting_keyboard())

async def insert_wiating_user(call : types.CallbackQuery):
    await sql_worker.insert_visitor(call.data.split(",")[0], call.data.split(",")[1], "visitors", "time_interval")
    await bot.send_message(call.from_user.id, "Пользователь добавлен")
    await bot.send_message(call.data.split(",")[0], f"Администратор вас добавил в {yaml_worker.get_button_name(call.data.split(',')[1])}")

def register_handlers_client(dp : Dispatcher):
    dp.register_callback_query_handler(insert_wiating_user,  button_filter.isModer(), lambda query: query.data.split(",")[2] == "Принять")
    dp.register_message_handler(registration_visitors, button_filter.isModer(), commands = "Зарегистрировать_пользователя")