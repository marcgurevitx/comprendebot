import asyncio
import pathlib

import click

from botcommon.config import config
from botcommon.models import Person, Phrase, Voice
from botcommon.s3 import retrieve_binary


@click.command()
@click.option("--start", type=click.DateTime())
@click.option("--end", type=click.DateTime())
@click.argument("person_id", type=int)
def botsubmissions(person_id, start, end):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_export_submissions(person_id, start, end))


async def async_export_submissions(person_id, start, end):
    person = await Person.select_one(id=person_id)
    if person is None:
        raise click.ClickException(f"No person with ID [{person_id}]")

    folder = pathlib.Path(config.CMPDBOT_EXCHANGE_DIR_CONTAINER, f"person__{person_id}")
    folder.mkdir(exist_ok=True)

    sql_where_list = []
    if start:
        sql_where_list.append(f"AND created_ts >= %(start)s")
    if end:
        sql_where_list.append(f"AND created_ts <= %(end)s")
    sql_where = " ".join(sql_where_list)

    phrases = await Phrase.select_sql_all(
        f"""
            SELECT
                *
            FROM
                {Phrase.get_table_name()}
            WHERE
                person_id = %(person_id)s
                {sql_where}
            ;
        """,
        **locals(),
    )
    for phrase in phrases:
        file_name = get_phrase_file_name(phrase)
        with open(folder / file_name, "w") as fp:
            fp.write(phrase.row.original_text)

    voices = await Voice.select_sql_all(
        f"""
            SELECT
                *
            FROM
                {Voice.get_table_name()}
            WHERE
                person_id = %(person_id)s
                {sql_where}
            ;
        """,
        **locals(),
    )
    for voice in voices:
        phrase = await Phrase.select_one(id=voice.row.phrase_id)
        file_name = get_voie_file_name(voice, phrase.row.normalized_text)
        voice_binary = await retrieve_binary(voice.row.s3_key)
        with open(folder / file_name, "wb") as fp:
            fp.write(voice_binary)

    click.echo(f"Done, phrases [{len(phrases)}], voices [{len(voices)}]")


def get_phrase_file_name(phrase):
    created_str = phrase.row.created_ts.strftime("%Y-%m-%d_%H-%M-%S")
    active_str = "V" if phrase.row.is_active else "X"
    id_str = phrase.row.id
    text_str = phrase.row.normalized_text.replace(" ", "-")
    return f"{created_str}__{active_str}__phr-{id_str}__{text_str}.txt"


def get_voie_file_name(voice, normalized_text):
    created_str = voice.row.created_ts.strftime("%Y-%m-%d_%H-%M-%S")
    active_str = "V" if voice.row.is_active else "X"
    id_str = voice.row.id
    text_str = normalized_text.replace(" ", "-")
    return f"{created_str}__{active_str}__voc-{id_str}__{text_str}.ogg"
