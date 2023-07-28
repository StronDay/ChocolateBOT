from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from services import yaml_worker

button_info_session = KeyboardButton("Инфо о текущей сессии")

def get_reg_keyboard(button_name):
    button_registration = InlineKeyboardButton("Регистрация", callback_data = button_name + ",Регистрация")
    reg_keyboard = InlineKeyboardMarkup()
    return reg_keyboard.row(button_registration)


def get_inline_keyboard(button_name):
    inline_button_1 = InlineKeyboardButton("Узнать кол-во поситителей", callback_data = button_name + ",Узнать")
    inline_button_2 = InlineKeyboardButton("Записаться", callback_data = button_name + ",Записаться")

    inline_keyboard = InlineKeyboardMarkup()
    inline_keyboard.row(inline_button_1)
    inline_keyboard.row(inline_button_2)

    return inline_keyboard

def get_client_keyboard():
    return yaml_worker.get_hobby_button_reply().row(button_info_session)