from botcommon.models import get_person_class


async def on_start(message):
    Person = get_person_class()
    person = await Person.find_or_create(
        telegram_uid=message.from_user.id,
        telegram_info=message.from_user.as_json(),
    )
    challenge = await person.get_new_challenge()

    # TODO: check challenge is None
    # TODO: challenge.get_reply() -> text/markup/keyboard...

    await message.reply("[TTT] welcome (back), id=%s! A new challenge for you: %s" % (person.row.id, challenge))


async def on_text(message):
    await message.reply("Hello i bot!")
