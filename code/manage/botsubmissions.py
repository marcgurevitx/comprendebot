import asyncio
import datetime
import pathlib

import click

from botcommon.config import config
from botcommon.models import Challenge, Phrase, Voice, Transcription
from botcommon.s3 import retrieve_binary


@click.command()
@click.option("-u", "--user", "person_id", type=int)
@click.option("-d", "--days", type=int)
@click.option("--start", "start", type=click.DateTime())
def botsubmissions(person_id, days, start):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_export_submissions(person_id, days, start))


async def async_export_submissions(person_id, days, start):
    if days:
        seconds = days * 24 * 60 * 60
    else:
        seconds = config.CHOOSE_HOLD_SECONDS + 24 * 60 * 60

    if start:
        end = start + datetime.timedelta(seconds=seconds)
    else:
        end = datetime.datetime.now()
        start = end - datetime.timedelta(seconds=seconds)

    start_str = start.strftime("%Y-%m-%d_%H-%M-%S")
    end_str = end.strftime("%Y-%m-%d_%H-%M-%S")
    folder = pathlib.Path(config.CMPDBOT_EXCHANGE_DIR_CONTAINER, f"sub_{start_str}_{end_str}_{person_id or 'all'}")
    folder.mkdir(exist_ok=True)

    sql_where_list = []
    if person_id:
        sql_where_list.append("AND person_id = %(person_id)s")
    sql_where = " ".join(sql_where_list)

    challenges = await Challenge.select_sql_all(
        f"""
            SELECT
                *
            FROM
                {Challenge.get_table_name()}
            WHERE
                created_ts >= %(start)s
                AND created_ts < %(end)s
                {sql_where}
            ;
        """,
        **locals(),
    )
    n_phrases = 0
    n_voices = 0
    n_transcriptions = 0
    for challenge in challenges:
        if challenge.row.type_code == 'CHL_PHR':
            n_phrases += 1
            await export_phrase(challenge, folder)
        elif challenge.row.type_code == 'CHL_VOC':
            n_voices += 1
            await export_voice(challenge, folder)
        elif challenge.row.type_code == 'CHL_TRS':
            n_transcriptions += 1
            await export_transcription(challenge, folder)

    click.echo(f"Done, phrases [{n_phrases}], voices [{n_voices}], transcriptions [{n_transcriptions}]")


def get_phrase_file_name(phrase, challenge):
    return "%(dt)s__%(activity_tag)s__%(person_id)s__%(id)s__%(normalized_text)s.txt" % dict(
        dt=challenge.row.created_ts.strftime("%Y-%m-%d_%H-%M-%S"),
        id=phrase.row.id,
        person_id=phrase.row.person_id,
        activity_tag="V" if phrase.row.is_active else "X",
        normalized_text=phrase.row.normalized_text.replace(" ", "-"),
    )


def get_voice_file_name(voice, phrase, challenge):
    return "%(dt)s__%(activity_tag)s__%(person_id)s__%(id)s__%(normalized_text)s.ogg" % dict(
        dt=challenge.row.created_ts.strftime("%Y-%m-%d_%H-%M-%S"),
        id=voice.row.id,
        person_id=voice.row.person_id,
        activity_tag="V" if voice.row.is_active else "X",
        normalized_text=phrase.row.normalized_text.replace(" ", "-"),
    )


def get_transcription_file_name(transcription, phrase, challenge):
    return "%(dt)s__%(activity_tag)s__%(person_id)s__t-%(id)s__%(normalized_text)s.txt" % dict(
        dt=challenge.row.created_ts.strftime("%Y-%m-%d_%H-%M-%S"),
        id=transcription.row.id,
        person_id=transcription.row.person_id,
        activity_tag="V" if transcription.row.is_active else "X",
        normalized_text=phrase.row.normalized_text.replace(" ", "-"),
    )


async def export_phrase(challenge, folder):
    phrase = await Phrase.select_one(challenge_id=challenge.row.id)
    if phrase:
        file_name = get_phrase_file_name(phrase, challenge)
        with open(folder / file_name, "w") as fp:
            fp.write(phrase.row.original_text)


async def export_voice(challenge, folder):
    voice = await Voice.select_one(challenge_id=challenge.row.id)
    if voice:
        voice_binary = await retrieve_binary(voice.row.s3_key)
        phrase = await Phrase.select_one(id=voice.row.phrase_id)
        file_name = get_voice_file_name(voice, phrase, challenge)
        with open(folder / file_name, "wb") as fp:
            fp.write(voice_binary)


async def export_transcription(challenge, folder):
    transcription = await Transcription.select_one(challenge_id=challenge.row.id)
    if transcription:
        voice = await Voice.select_one(id=transcription.row.voice_id)
        phrase = await Phrase.select_one(id=voice.row.phrase_id)
        file_name = get_transcription_file_name(transcription, phrase, challenge)
        with open(folder / file_name, "w") as fp:
            fp.write(transcription.row.user_text)
