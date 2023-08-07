from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from services import yaml_worker
from aiogram.utils.callback_data import CallbackData

cd_time = CallbackData("time_px", "time")
cd_registration = CallbackData("reg_px", "button")

cd_amount_vis = CallbackData("amount_px", "button")
cd_insert_vis = CallbackData("insert_px", "button")


button_info_session = KeyboardButton("Узнать о текущей тренировке")

button_extend_inline = InlineKeyboardButton("Продлить", callback_data="Продлить")
button_complete_inline = InlineKeyboardButton("Завершить", callback_data="Завершить")

training_choise_keyboard = InlineKeyboardMarkup()
training_choise_keyboard.row(button_extend_inline, button_complete_inline)

button_time_15min = InlineKeyboardButton("15мин", callback_data = cd_time.new(time = "15"))
button_time_30min = InlineKeyboardButton("30мин", callback_data = cd_time.new(time = "30"))
button_time_45min = InlineKeyboardButton("45мин", callback_data = cd_time.new(time = "45"))
button_time_1hour = InlineKeyboardButton("1час", callback_data = cd_time.new(time = "60"))

button_time_1hour15min = InlineKeyboardButton("1час 15мин", callback_data = cd_time.new(time = "75"))
button_time_1hour30min = InlineKeyboardButton("1час 30мин", callback_data = cd_time.new(time = "90"))
button_time_1hour45min = InlineKeyboardButton("1час 45мин", callback_data = cd_time.new(time = "105"))
button_time_2hour = InlineKeyboardButton("2часа", callback_data = cd_time.new(time = "120"))

time_keyboard = InlineKeyboardMarkup()
time_keyboard.row(button_time_15min, button_time_30min, button_time_45min, button_time_1hour)
time_keyboard.row(button_time_1hour15min, button_time_1hour30min, button_time_1hour45min, button_time_2hour)

def get_reg_keyboard(button_name):
    button_registration = InlineKeyboardButton("Регистрация", callback_data = cd_registration.new(button = button_name))
    reg_keyboard = InlineKeyboardMarkup()
    return reg_keyboard.row(button_registration)


def get_inline_keyboard(button_name):
    inline_button_1 = InlineKeyboardButton("Узнать кол-во поситителей", callback_data = cd_amount_vis.new(button = button_name))
    inline_button_2 = InlineKeyboardButton("Записаться", callback_data = cd_insert_vis.new(button = button_name))

    inline_keyboard = InlineKeyboardMarkup()
    inline_keyboard.row(inline_button_1)
    inline_keyboard.row(inline_button_2)

    return inline_keyboard

def get_client_keyboard():
    return yaml_worker.get_hobby_button_reply().row(button_info_session)