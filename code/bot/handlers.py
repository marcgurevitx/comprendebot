import string

from aiogram.types import ContentType

from bot.decos import with_person_and_chat
from bot.helpers import arrange_new_challenge, download_voice
from botcommon.config import config


@with_person_and_chat
async def on_cmd_start(message, *, person, chat, **kwargs):
    await arrange_new_challenge(person, chat)


@with_person_and_chat
async def on_message(message, *, person, chat, **kwargs):
    challenge = await person.get_existing_active_challenge()
    if challenge:
        async with challenge.get_executor() as executor:
            if message.content_type == ContentType.VOICE:
                await executor.receive_voice(message.voice, message.message_id)
            elif message.content_type == ContentType.TEXT:
                await executor.receive_text(message.text, message.message_id)
            else:
                pass
            sendables = executor.pop_sendables()
            await chat.send_list(sendables)
    else:
        tr = string.Template(_("Send /$cmd_start for new challenge.  // no active challenges"))
        tr = tr.substitute(
            cmd_start=_("start  // command"),
        )
        await message.reply(tr)


@with_person_and_chat
async def on_button_press(callback_query, *, person, chat, **kwargs):
    if callback_query.data == config.CMPDBOT_CONST_START:
        await callback_query.answer(_("Starting...  // caption after start press"))
        return await arrange_new_challenge(person, chat)

    challenge = await person.get_existing_active_challenge()
    if challenge:
        await callback_query.answer(_("Processing...  // caption after button press"))
        async with challenge.get_executor() as executor:
            message = callback_query.message.reply_to_message
            if message is None:
                await executor.receive_button_press_on_nothing(callback_query.data)
            elif message.content_type == ContentType.VOICE:
                voice_bytes = await download_voice(message.voice)
                await executor.receive_button_press_on_voice(
                    message.voice.file_unique_id,
                    voice_bytes,
                    callback_query.data,
                )
            elif message.content_type == ContentType.TEXT:
                await executor.receive_button_press_on_text(message.text, callback_query.data)
            else:
                pass
            sendables = executor.pop_sendables()
            await chat.send_list(sendables)
    else:
        await callback_query.answer("?")
