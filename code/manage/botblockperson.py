import asyncio

import click

from botcommon.models import Person, Phrase, Voice


@click.command()
@click.option("--unblock", is_flag=True)
@click.argument("person_id", type=int)
def botblockperson(person_id, unblock):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_block_person(person_id, unblock))


async def async_block_person(person_id, unblock):
    if unblock:
        new_is_active = True
        done_str = "unblocked"
    else:
        new_is_active = False
        done_str = "blocked"

    person = await Person.select_one(id=person_id)
    if not person:
        raise click.ClickException(f"No person with ID [{person_id}]")
    await person.update(is_active=new_is_active)

    phrases = await Phrase.select_all(person_id=person_id)
    n_far_voices = 0
    for phrase in phrases:
        await phrase.update(is_active=new_is_active)
        for voice in await Voice.select_all(person_id=phrase.person_id):
            n_far_voices += 1
            await voice.update(is_active=new_is_active)

    voices = await Voice.select_all(person_id=person_id)
    for voice in voices:
        await voice.update(is_active=new_is_active)

    click.echo(f"Done, phrases [{len(phrases)} {done_str}], voices [{len(voices) + n_far_voices} {done_str}]")
