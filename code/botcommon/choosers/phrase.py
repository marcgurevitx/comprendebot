import logging
import math
import random

from goodenough import GoodEnough

from botcommon.config import config
from botcommon.db import get_pg_cursor

logger = logging.getLogger(__name__)

REALLY_LONG_PHRASE = 1000


async def get_items(request):
    from botcommon.models.phrase import Phrase

    percent = min(
        config.CMPDBOT_CHALLENGE_SAMPLE_PHRASE / (await Phrase.count(is_active=True) or 1) * 100,
        100,
    )

    logger.debug("Sample percent [%r]", percent)

    sql_exclude = " ".join(
        f", {p}"
        for p
        in request["exclude_phrases"]
    )
    async with get_pg_cursor() as cur:
        await cur.execute(
            f"""
                SELECT
                    *
                FROM
                    {Phrase.get_table_name()} TABLESAMPLE BERNOULLI ({percent})
                WHERE
                    is_active = true
                    AND id NOT IN (0 {sql_exclude})
                ;
            """,
        )
        rows = await cur.fetchall()

    logger.debug("Sample size [%r]", len(rows))

    return [Phrase(r) for r in rows]


async def ensure_not_dummy(request, phrase):
    if phrase.row.original_text == "":
        return 0.0
    return 1.0


async def ensure_person_level(request, phrase):
    success = request["person_n_prev_success"] + config.CMPDBOT_CHALLENGE_SUCCESS_BOOST
    length_diff = abs(success - len(phrase.row.normalized_text))
    length_log = math.log10(length_diff + 1)
    return 1 - length_log


async def ensure_shortest(request, phrase):
    length_log = math.log(
        len(phrase.row.normalized_text),
        REALLY_LONG_PHRASE,
    )
    return 1 - length_log


async def ensure_random(request, phrase):
    return random.random()


async def ensure_same_author_rare(request, phrase):
    if request["person_id"] == phrase.row.person_id:
        return 0.8
    return 1.0


fair_phrase_chooser = GoodEnough(
    get_items=get_items,
    rules={
        ensure_not_dummy: 1.0,
        ensure_person_level: 1.0,
        ensure_same_author_rare: 1.0,
    },
)

easy_phrase_chooser = GoodEnough(
    get_items=get_items,
    rules={
        ensure_not_dummy: 1.0,
        ensure_shortest: 1.0,
        ensure_same_author_rare: 1.0,
    },
)

random_phrase_chooser = GoodEnough(
    get_items=get_items,
    rules={
        ensure_not_dummy: 1.0,
        ensure_random: 1.0,
        ensure_same_author_rare: 1.0,
    },
)
