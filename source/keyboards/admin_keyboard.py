from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup ,InlineKeyboardButton
from services import yaml_worker

button_admin = KeyboardButton("/Панель_администратора")
button_default = KeyboardButton("/Обычная_панель")
button_all_info_button = KeyboardButton("/Инфа_все_кнопки")
button_add_visitor =  KeyboardButton("/Зарегистрировать_пользователя")
button_sql = KeyboardButton("/Управление_рассылкой")

button_change_name = KeyboardButton("/Изменить_название")
button_change_location = KeyboardButton("/Изменить_локацию")
button_add = KeyboardButton("/Добавить_кнопку")
button_delete = KeyboardButton("/Удалить_кнопку")

button_cancel = InlineKeyboardButton("Отменить", callback_data = "Отменить,Отменить")
button_cancel_cancel = InlineKeyboardButton("Отменить", callback_data= "Отменить,Отменить,Отменить")

button_save_visitors = KeyboardButton("/Записать_новых_пользователей_в_бд")
button_malling = KeyboardButton("/Сделать_рассылку")

malling_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
malling_keyboard.row(button_malling)
malling_keyboard.row(button_save_visitors)
malling_keyboard.row(button_admin)

def keyboard_admin_default():
    return yaml_worker.get_hobby_buttons_replay().row(button_admin)

def get_buttons(action):
    return yaml_worker.get_hobby_buttons_inline(action).add(button_cancel)

def get_all_button_info_inline(action):
    return yaml_worker.get_hobby_location_inline(action)

def get_buttons_pallet(action):
    return yaml_worker.get_hobby_buttons_pallet(action).row(button_cancel_cancel)

keyboard_admin_admin = ReplyKeyboardMarkup(resize_keyboard = True)

keyboard_admin_admin.row(button_add, button_delete)
keyboard_admin_admin.row(button_change_name, button_change_location)
keyboard_admin_admin.row(button_all_info_button)
keyboard_admin_admin.row(button_add_visitor)
keyboard_admin_admin.row(button_sql)
keyboard_admin_admin.row(button_default)