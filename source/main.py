import asyncio

from aiogram.utils import executor
from create_bot import dp
from handlers import client, admin, general, moderator
from data_base import sql_worker
from services import script_worker


async def on_startup(_):
    print("Бот вышел в онлайн")

sql_worker.sql_start()


general.register_handlers_client(dp)
admin.register_handlers_client(dp)
client.register_handlers_client(dp)
moderator.register_handlers_client(dp)

loop = asyncio.get_event_loop()
loop.create_task(script_worker.schedule_task())

executor.start_polling(dp, skip_updates = True, on_startup = on_startup)
sql_worker.sql_close()