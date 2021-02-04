from botcommon.models import Person


async def on_start(message):
    person = await Person.find_or_create(
        telegram_uid=message.from_user.id,
        telegram_info=message.from_user.as_json(),
    )
    challenge = await person.get_new_challenge()
    if challenge is None:
        await message.bot.send_message(
            chat_id=message.chat.id,
            text="[TTT] No challenge can be found. Please try later.",
        )

    # TODO: check challenge is None
    # TODO: challenge.get_reply() -> text/markup/keyboard...

    await message.reply("[TTT] welcome (back), id=%s! A new challenge for you: %s" % (person.row.id, challenge))


async def on_text(message):
    await message.reply("Hello i bot!")
