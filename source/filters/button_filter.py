import os
from aiogram import types
from aiogram.dispatcher.filters import Filter
from dotenv import load_dotenv
from services import yaml_worker

load_dotenv()

# class Filter_values(Filter):
    
#     key="filter_values"

#     def __init__(self, value, position) -> None:
#         super().__init__()

#         self.value = value
#         self.position = position

#     async def check(self, call: types.CallbackQuery) -> bool:
#         return call.data.split(",")[self.position] == self.value
    
class isAdmin(Filter):

    key = 'is_admin_filter'

    async def check(self, call: types.CallbackQuery) -> bool:
        return call.from_user.id ==  int(os.getenv("ADMIN_ID"))
    
class isModer(Filter):

    key = 'is_moder_filter'

    async def check(self, call: types.CallbackQuery) -> bool:
        return call.from_user.id ==  int(os.getenv("MODERATOR_ID")) or call.from_user.id ==  int(os.getenv("ADMIN_ID"))
    
class isHobbyButton(Filter):

    key = 'is_hobby_button_filter'

    async def check(self, message : types.Message) -> bool:
        return yaml_worker.is_hobby_button(message.text)