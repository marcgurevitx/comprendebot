import logging
import os

from aiogram import Bot, Dispatcher, executor, types

from bot.handlers import (
    on_start,
    on_text,
    on_edit,
)
from botcommon.config import config

logging.basicConfig(level=config.LOG_LEVEL)

bot = Bot(token=config.CMPDBOT_TOKEN)

dp = Dispatcher(bot)
dp.register_message_handler(on_start, commands=["start"])
dp.register_message_handler(on_text)
dp.register_edited_message_handler(on_edit)


async def on_startup(dp):
    await bot.set_my_commands([
        types.BotCommand(command="/start", description="[TTT] Start/restart"),
        types.BotCommand(command="/xxx", description="[TTT] Xxx"),
        types.BotCommand(command="/aaa", description="[TTT] Aaa"),
    ])


if config.MIGRATIONS_SYNC:
    os.system("$CMPDBOT_DIR/extlibs/vishnubob-wait-for-it/wait-for-it.sh -s $MIGRATIONS_HOST:$MIGRATIONS_PORT")

executor.start_polling(dp, on_startup=on_startup)
