import os
from aiogram import types
from aiogram.dispatcher.filters import Filter
from dotenv import load_dotenv
from services import yaml_worker

load_dotenv()

class DeleteButtonFilter(Filter):

    key = 'delete_filter'

    async def check(self, call: types.CallbackQuery) -> bool:
        return call.data.split(",")[1] == "delete"
    
class ChangeButtonFilter(Filter):

    key = 'change_filter'

    async def check(self, call: types.CallbackQuery) -> bool:
        return call.data.split(",")[1] == "change"

class ChangeButtonLocationFilter(Filter):

    key = 'change_location_filter'

    async def check(self, call: types.CallbackQuery) -> bool:
        return call.data.split(",")[1] == "change_location"
    
class AddButtonFilter(Filter):

    key = 'add_filter'

    async def check(self, call: types.CallbackQuery) -> bool:
        return call.data.split(",")[2] == "add"
    
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
    
class isInsert(Filter):

    key = 'is_insert'

    async def check(self, call: types.CallbackQuery) -> bool:
        return call.data.split(",")[1] == "Записаться"
    
class isAmount(Filter):

    key = 'is_amount'

    async def check(self, call: types.CallbackQuery) -> bool:
        return call.data.split(",")[1] == "Узнать"
    
class isAccept(Filter):

    key = 'is_accept'

    async def check(self, call: types.CallbackQuery) -> bool:
        return call.data.split(",")[2] == "Принять"