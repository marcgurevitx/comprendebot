import datetime

from aiogram import types

from botcommon.person import Person


async def on_start(message):
    person = await Person.find(message.from_user.id)
    if person is None:
        person = await Person.insert(
            is_active=True,
            telegram_uid=message.from_user.id,
            telegram_info=message.from_user.as_json(),
            started_ts=datetime.datetime.now(),
        )
    await message.reply("[TTT] welcome (back), id=%s!" % person.row.id)


async def on_text(message):
    await message.reply("Hello i bot!")
