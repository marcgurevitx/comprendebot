import logging

from aiogram import Bot, Dispatcher, executor

from bot.handlers import on_text
from botcommon.config import config

logging.basicConfig(level=config.LOG_LEVEL)

bot = Bot(token=config.CMPDBOT_TOKEN)

dp = Dispatcher(bot)
dp.register_message_handler(on_text)

executor.start_polling(dp)
