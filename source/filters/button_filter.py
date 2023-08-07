import os
from aiogram import types
from aiogram.dispatcher.filters import Filter
from dotenv import load_dotenv
from services import yaml_worker

load_dotenv()

def is_valid_id(user_id, name_env_vr) -> bool:
    id_admin_str = os.getenv(name_env_vr)
    id_admin_list = [int(id) for id in id_admin_str.split(",")]

    for id in id_admin_list:
        if user_id == id:
            return True

    return False

def is_admin(user_id) -> bool:
    return is_valid_id(user_id, "ADMIN_ID")

def is_moder(user_id) -> bool:
    return is_valid_id(user_id, "MODERATOR_ID")
    
class isAdmin(Filter):

    key = 'is_admin_filter'

    async def check(self, call: types.CallbackQuery) -> bool:
        return is_admin(call.from_user.id)
    
class isModer(Filter):

    key = 'is_moder_filter'

    async def check(self, call: types.CallbackQuery) -> bool:
        return is_moder(call.from_user.id) or is_admin(call.from_user.id)
    
class isHobbyButton(Filter):

    key = 'is_hobby_button_filter'

    async def check(self, message : types.Message) -> bool:
        return yaml_worker.is_hobby_button(message.text)