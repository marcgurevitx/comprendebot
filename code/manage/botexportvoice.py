import asyncio
import pathlib

import click

from botcommon.config import config
from botcommon.models import Voice
from botcommon.s3 import retrieve_binary

DEFAULT_OUT_DIR_NAME = "outoggs/"


@click.command()
@click.option("-d", "--output-dir", "output_dir", type=click.Path(file_okay=False, writable=True))
@click.argument("voice_ids")
def botexportvoice(output_dir, voice_ids):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_export_voice(output_dir, voice_ids))


async def async_export_voice(output_dir, voice_ids):
    if not output_dir:
        output_dir = pathlib.Path(config.CMPDBOT_EXCHANGE_DIR_CONTAINER, DEFAULT_OUT_DIR_NAME)
    output_dir.mkdir(parents=True, exist_ok=True)

    voice_ids_tuple = tuple(int(x) for x in voice_ids.split())
    voices = await Voice.select_sql_all(
        f"""
            SELECT
                *
            FROM
                {Voice.get_table_name()}
            WHERE
                id in %(voice_ids)s
            ;
        """,
        voice_ids=voice_ids_tuple,
    )

    for voice in voices:
        voice_binary = await retrieve_binary(voice.row.s3_key)
        with open(output_dir / f"{voice.row.id}.ogg", "wb") as fp:
            fp.write(voice_binary)

    click.echo(f"Done, output_dir = [{output_dir}]")
