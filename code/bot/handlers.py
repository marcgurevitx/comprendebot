import datetime

from botcommon.models.person import Person


async def on_start(message):
    person = await Person.select_one(telegram_uid=message.from_user.id)
    if person is None:
        person = await Person.insert(
            is_active=True,
            created_ts=datetime.datetime.now(),
            telegram_uid=message.from_user.id,
            telegram_info=message.from_user.as_json(),
        )
    challenge = await person.get_new_challenge()

    # TODO: check challenge is None
    # TODO: challenge.get_reply() -> text/markup/keyboard...

    await message.reply("[TTT] welcome (back), id=%s! A new challenge for you: %s" % (person.row.id, challenge))


async def on_text(message):
    await message.reply("Hello i bot!")
