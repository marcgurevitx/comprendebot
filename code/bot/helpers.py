import datetime
import io

from aiogram.types import CallbackQuery

from bot.chat import Chat
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
        await chat.send_simple_text("[TTT] No challenge found. Please try later.")
    else:
        async with challenge.get_executor() as executor:
            await executor.start()
            sendables = executor.pop_sendables()
            await chat.send_list(sendables)


async def download_voice(voice):
    voice_io = await voice.download(destination=io.BytesIO())
    voice_bytes = voice_io.read()
    return voice_bytes
