import os
import asyncio

from services import script_worker
from dotenv import load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot
from aiogram.dispatcher import Dispatcher

load_dotenv()

loop = asyncio.get_event_loop()
loop.create_task(script_worker.schedule_task())

bot = Bot(os.getenv("TOKEN"), loop=loop)

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)