import logging
import math
import random

from goodenough import GoodEnough

from botcommon.config import config
from botcommon.db import get_pg_cursor

logger = logging.getLogger(__name__)

REALLY_LONG_PHRASE = 1000


async def get_items(request):
    from botcommon.models.voice import Voice

    percentage = min(
        config.CMPDBOT_CHALLENGE_SAMPLE_VOICE / (await Voice.count(is_active=True) or 1) * 100,
        100,
    )

    logger.debug("Sample percentage [%r]", percentage)

    sql_exclude = " ".join(
        f", {v}"
        for v
        in request["exclude_voices"]
    )
    async with get_pg_cursor() as cur:
        await cur.execute(
            f"""
                SELECT
                    *
                FROM
                    {Voice.get_table_name()} TABLESAMPLE BERNOULLI ({percentage})
                WHERE
                    is_active = true
                    AND id NOT IN (0 {sql_exclude})
                ;
            """,
        )
        rows = await cur.fetchall()

    logger.debug("Sample size [%r]", len(rows))

    return [Voice(r) for r in rows]


async def ensure_not_dummy(request, voice):
    if voice.row.length == 0:
        return 0.0
    return 1.0


async def ensure_person_level(request, voice):
    success = request["person_n_prev_success"] + config.CMPDBOT_CHALLENGE_SUCCESS_BOOST
    length_diff = abs(success - voice.row.length)
    length_log = math.log10(length_diff + 1)
    return 1 - length_log


async def ensure_shortest(request, voice):
    length_log = math.log(
        voice.row.length,
        REALLY_LONG_PHRASE,
    )
    return 1 - length_log


async def ensure_random(request, voice):
    return random.random()


async def ensure_same_author_rare(request, voice):
    if request["person_id"] == voice.row.person_id:
        return 0.8
    return 1.0


async def ensure_repetition_rare(request, voice):
    from botcommon.models.transcription import Transcription

    if await Transcription.select_one(person_id=request["person_id"], voice_id=voice.row.id):
        return 0.1
    return 1.0


_common_rules = {
    ensure_not_dummy: 1.0,
    ensure_same_author_rare: 1.0,
    ensure_repetition_rare: 1.0,
}

fair_voice_chooser = GoodEnough(
    get_items=get_items,
    rules={
        **_common_rules,
        ensure_person_level: 1.0,
    },
)

easy_voice_chooser = GoodEnough(
    get_items=get_items,
    rules={
        **_common_rules,
        ensure_shortest: 1.0,
    },
)

random_voice_chooser = GoodEnough(
    get_items=get_items,
    rules={
        **_common_rules,
        ensure_random: 1.0,
    },
)
