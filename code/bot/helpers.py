import datetime
import io

from aiogram.types import CallbackQuery

from bot.chat import Chat
from botcommon.bottypes import Sendable, SendableTypeCode
from botcommon.config import config
from botcommon.helpers import get_start_button
from botcommon.models import Person


def get_chat(entity):
    if isinstance(entity, CallbackQuery):
        message = entity.message
    else:
        message = entity
    return Chat(message.bot, message.chat.id, message)


async def get_person(entity):
    return await Person.select_one(telegram_uid=entity.from_user.id)


async def create_person(entity):
    return await Person.insert(
        is_active=True,
        created_ts=datetime.datetime.now(),
        telegram_uid=entity.from_user.id,
        telegram_info=entity.from_user.as_json(),
    )


async def arrange_new_challenge(person, chat):
    challenge = await person.get_new_challenge()
    if challenge is None:
        await chat.send_simple_text(_("No challenge found. Please try later."))
    else:
        async with challenge.get_executor() as executor:
            await executor.start()
            sendables = executor.pop_sendables()
            await chat.send_list(sendables)


async def download_voice(voice):
    voice_io = await voice.download(destination=io.BytesIO())
    voice_bytes = voice_io.read()
    return voice_bytes


async def welcome_new_user(person, chat):
    me = await chat.bot.get_me()
    s = Sendable(
        type=SendableTypeCode.SND_TXT,
        value=_(
            "Hello, I'm %(botname)s."
            " I help people test their ability to understand spoken language"
            " (the language is <a href=\"%(language_link)s\">%(language)s</a>)."
            " For more info see %(bot_info_link)s."
            " Press start button or send /%(cmd_start)s for your first challenge."
        ) % {
            "botname": me.first_name,
            "language": config.CMPDBOT_LANGUAGE_HUMANS,
            "language_link": config.CMPDBOT_LANGUAGE_SITE,
            "bot_info_link": config.CMPDBOT_LINK,
            "cmd_start": _("start  // command"),
        },
        is_reply=False,
        buttons=[get_start_button()],
    )
    await chat.send(s)
