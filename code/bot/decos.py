import datetime

from bot.chat import Chat
from bot.helpers import arrange_new_challenge
from botcommon.models import Person


def with_person_and_chat(handler):

    async def handler_with_person(message, *args, **kwargs):
        chat = Chat(message.bot, message.chat.id, message)
        person = await Person.select_one(telegram_uid=message.from_user.id)
        if person is not None:
            return await handler(message, person=person, chat=chat, *args, **kwargs)
        person = await Person.insert(
            is_active=True,
            created_ts=datetime.datetime.now(),
            telegram_uid=message.from_user.id,
            telegram_info=message.from_user.as_json(),
        )
        await arrange_new_challenge(person, chat)

    return handler_with_person
