import os
from dotenv import load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot
from aiogram.dispatcher import Dispatcher

load_dotenv()

bot = Bot(os.getenv("TOKEN"))

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)