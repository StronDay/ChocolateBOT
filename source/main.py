import asyncio
import os

from aiogram.utils import executor
from create_bot import dp, bot
from handlers import client, admin, general, moderator
from data_base import sql_worker
from services import script_worker

async def on_startup(dp):
    await bot.set_webhook(os.getenv("URL_APP"))
    print("[INFO] Бот вышел в онлайн")

async def on_shutdown(dp):
    print("[INFO] Бот выключился")
    await bot.delete_webhook()

sql_worker.sql_start()

general.register_handlers_client(dp)
admin.register_handlers_client(dp)
client.register_handlers_client(dp)
moderator.register_handlers_client(dp)

loop = asyncio.get_event_loop()
loop.create_task(script_worker.schedule_task())

#executor.start_polling(dp, skip_updates = True, on_startup = on_startup)
executor.start_webhook(
    dispatcher = dp,
    webhook_path='',
    on_startup=on_startup,
    on_shutdown=on_shutdown,
    skip_updates=True,
    host='0.0.0.0',
    port=int(os.environ.get("PORT", 5000))
)
sql_worker.sql_close()