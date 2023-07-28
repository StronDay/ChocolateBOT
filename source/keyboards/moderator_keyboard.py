from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from services import yaml_worker
from data_base import sql_worker

register_button = KeyboardButton("/Зарегистрировать_пользователя")
moderator_keyboard = ReplyKeyboardMarkup(resize_keyboard = True)
moderator_keyboard.row(register_button)

def get_waiting_keyboard():
    return sql_worker.get_waiting_keyboard()

