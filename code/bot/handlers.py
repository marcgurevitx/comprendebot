from bot.chat import Chat
from botcommon.models import Person


async def on_start(message):
    chat = Chat(message.bot, message.chat.id)
    person = await Person.find_or_create(
        telegram_uid=message.from_user.id,
        telegram_info=message.from_user.as_json(),
    )
    challenge = await person.get_new_challenge()
    if challenge is None:
        await chat.send_text("[TTT] No challenge found. Please try later.")
    else:
        sendable = await challenge.start()
        await chat.send(sendable)


async def on_text(message):
    await message.reply("Hello i bot!")
