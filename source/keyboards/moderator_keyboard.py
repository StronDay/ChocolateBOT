from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data_base import sql_worker
from services import yaml_worker
from aiogram.utils.callback_data import CallbackData
from keyboards import button_info_session

cd_accept = CallbackData("accept_px", "id_user", "location")
cd_code = CallbackData("code_px", "code")
cd_location = CallbackData("location_px", "location")


button_register = KeyboardButton("/Зарегистрировать_пользователя")
button_add_granny = KeyboardButton("/Добавить_бабулю")

def get_moderator_keyboard():
    moderator_keyboard = yaml_worker.get_hobby_buttons_replay()
    moderator_keyboard.row(button_info_session)
    moderator_keyboard.row(button_register)
    moderator_keyboard.row(button_add_granny)

    return moderator_keyboard

async def get_waiting_keyboard():
    result = await sql_worker.get_waiting_keyboard_sql()
    return result

