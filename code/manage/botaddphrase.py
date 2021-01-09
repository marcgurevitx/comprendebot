import asyncio

import click

from botcommon.db import get_pg_pool
from botcommon.language import Language
from botcommon.phrase import Phrase


@click.command()
@click.argument("phrase")
def botaddphrase(phrase):

    loop = asyncio.get_event_loop()

    language = Language.get_instance()
    normalized_text = language.normalize_text(phrase)
    similar = loop.run_until_complete(find_similar_phrases(normalized_text))

    should_add = True
    if similar:
        similar.sort(reverse=True)
        click.echo("Similar phrases found:")
        for rat, row in similar[:3]:
            click.secho(f"    (ratio={rat}) ", nl=False, fg="yellow")
            click.secho(f"{row}")
        if not click.confirm("Add anyway?"):
            should_add = False

    if should_add:
        loop.run_until_complete(
            insert_phrase(
                original_text=phrase,
                normalized_text=normalized_text,
            ),
        )
        click.secho("Added.", fg="green")
    else:
        click.secho("Not added.", fg="yellow")


async def find_similar_phrases(normalized_text):
    pool = await get_pg_pool()
    async with pool.acquire() as conn:
        similar = await Phrase.find_similar(conn, normalized_text)
    return similar


async def insert_phrase(**kwargs):
    pool = await get_pg_pool()
    async with pool.acquire() as conn:
        await Phrase.insert(conn, is_active=True, **kwargs)
