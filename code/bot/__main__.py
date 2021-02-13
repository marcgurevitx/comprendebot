import gettext
import logging
import os

from aiogram import Bot, Dispatcher, executor, types

from bot.handlers import (
    on_cmd_start,
    on_message,
    on_button_press,
)
from botcommon.config import config

lang = gettext.translation(
    "messages",
    config.CMPDBOT_LOCALE_DIR,
    languages=[config.CMPDBOT_LANGUAGE],
)
lang.install()

logging.basicConfig(level=config.LOG_LEVEL)

bot = Bot(token=config.CMPDBOT_TOKEN, parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot)
dp.register_message_handler(on_cmd_start, commands=["start", _("start  // command")])
dp.register_message_handler(on_message, content_types=[types.ContentType.TEXT, types.ContentType.VOICE])
dp.register_callback_query_handler(on_button_press)


async def on_startup(dp):
    description_start = _("start a new challenge  // command description")
    await bot.set_my_commands([
        types.BotCommand(command="/start", description=description_start),
        types.BotCommand(command="/" + _("start  // command"), description=description_start),
    ])


if config.MIGRATIONS_SYNC:
    os.system("$CMPDBOT_DIR/extlibs/vishnubob-wait-for-it/wait-for-it.sh -s $MIGRATIONS_HOST:$MIGRATIONS_PORT")

executor.start_polling(dp, on_startup=on_startup)
