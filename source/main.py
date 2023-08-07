import logging
import os

from dotenv import load_dotenv
from aiogram.utils import executor
from create_bot import dp, bot
from handlers import client, admin, general, moderator
from data_base import sql_worker

load_dotenv()

async def admin_malling(messege: str):
    id_admin_str = os.getenv("ADMIN_ID")
    id_admin_list = [int(id) for id in id_admin_str.split(",")]

    for id in id_admin_list:
        await bot.send_message(id, messege)

# webhook settings
WEBHOOK_HOST = os.getenv("URL_APP")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH")
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

print(f"[INFO] WEBHOOK_URL: {WEBHOOK_URL}")

# webserver settings
WEBAPP_HOST = 'localhost'
WEBAPP_PORT = 8443

logging.basicConfig(level=logging.INFO)

sql_worker.sql_start()

general.register_handlers_client(dp)
admin.register_handlers_client(dp)
client.register_handlers_client(dp)
moderator.register_handlers_client(dp)

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    await admin_malling("[START] Колясик вышел на смену!")
    print("[INFO] Бот вышел в онлайн")

async def on_shutdown(dp):
    await admin_malling("[STOP] Колясик решил отдохнуть :( ...)")
    print("[INFO] Бот выключился")
    sql_worker.sql_close()
    await bot.delete_webhook()

executor.start_webhook(
    dispatcher=dp,
    webhook_path=WEBHOOK_PATH, 
    on_startup=on_startup,
    on_shutdown=on_shutdown,
    skip_updates=True,
    host=WEBAPP_HOST, 
    port=WEBAPP_PORT
)