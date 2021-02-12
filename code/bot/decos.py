from bot.helpers import (
    get_chat,
    get_person,
    create_person,
    welcome_new_user,
)


def with_person_and_chat(handler):

    async def handler_with_person(entity, **kwargs):
        chat = get_chat(entity)
        person = await get_person(entity)

        if person is None:
            person = await create_person(entity)
            return await welcome_new_user(person, chat)

        await handler(entity, person=person, chat=chat, **kwargs)

    return handler_with_person
