import asyncio
import pathlib

import click

from botcommon.config import config
from botcommon.models import Voice
from botcommon.s3 import retrieve_binary

DEFAULT_OUT_FILE_NAME = "out.ogg"


@click.command()
@click.option("-o", "--output-file", "output_file", type=click.Path(dir_okay=False, writable=True))
@click.argument("voice_id", type=int)
def botexportvoice(output_file, voice_id):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_export_voice(output_file, voice_id))


async def async_export_voice(output_file, voice_id):
    voice = await Voice.select_one(id=voice_id)
    if not voice:
        raise click.ClickException(f"No voice with ID [{voice_id}]")

    if not output_file:
        output_file = pathlib.Path(config.CMPDBOT_EXCHANGE_DIR_CONTAINER, DEFAULT_OUT_FILE_NAME)

    voice_binary = await retrieve_binary(voice.row.s3_key)
    with open(output_file, "wb") as fp:
        fp.write(voice_binary)

    click.echo(f"Done, output_file = [{output_file}]")
