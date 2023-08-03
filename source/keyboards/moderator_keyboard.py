from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data_base import sql_worker
from aiogram.utils.callback_data import CallbackData

cd_accept = CallbackData("accept_px", "id_user", "location")
cd_code = CallbackData("code_px", "code")
cd_location = CallbackData("location_px", "location")


register_button = KeyboardButton("/Зарегистрировать_пользователя")
moderator_keyboard = ReplyKeyboardMarkup(resize_keyboard = True)
moderator_keyboard.row(register_button)

def get_waiting_keyboard():
    return sql_worker.get_waiting_keyboard()

