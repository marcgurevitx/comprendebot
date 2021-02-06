from bot.decos import with_person_and_chat
from bot.helpers import arrange_new_challenge


@with_person_and_chat
async def on_start(message, *, person, chat, **kwargs):
    await arrange_new_challenge(person, chat)


@with_person_and_chat
async def on_text(message, *, person, chat, **kwargs):
    challenge = await person.get_existing_active_challenge()
    if challenge is None:

        await message.reply("[TTT] Send /comensa for new challenge. Send /aida for help.")

        pass#?

    async with challenge.get_executor() as executor:
        await executor.receive_text(message.text)
        sendables = executor.pop_sendables()
        await chat.send_list(sendables)
