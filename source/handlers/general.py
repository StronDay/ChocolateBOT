from aiogram import types, Dispatcher
from create_bot import bot

from keyboards import keyboard_admin_default
from keyboards import get_client_keyboard
from keyboards import moderator_keyboard

import os
from dotenv import load_dotenv

load_dotenv()

#commands = "start"
async def command_start(message : types.Message):

    if message.from_user.id == int(os.getenv("ADMIN_ID")):
        await bot.send_message(message.from_user.id, "Приветствую, хозяин", reply_markup=keyboard_admin_default())
    elif message.from_user.id == int(os.getenv("MODERATOR_ID")):
        await bot.send_message(message.from_user.id, "Приветствую самого лучшего сотрудника😎", reply_markup=moderator_keyboard)
    else:
        await bot.send_message(message.from_user.id, "Привет", reply_markup=get_client_keyboard())

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands = "start")