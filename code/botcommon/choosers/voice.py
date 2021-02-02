import logging

from goodenough import GoodEnough

from botcommon.config import config
from botcommon.db import get_pg_cursor


async def get_items(request):
    from botcommon.models.voice import Voice

    percent = min(
        config.CMPDBOT_CHALLENGE_SAMPLE_VOICE / (await Voice.count(is_active=True) or 1) * 100,
        100,
    )

    logging.debug("Sample percent [%r]", percent)

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
                    {Voice.get_table_name()} TABLESAMPLE BERNOULLI ({percent})
                WHERE
                    is_active = true
                    AND id NOT IN (0 {sql_exclude})
                ;
            """,
        )
        rows = await cur.fetchall()

    logging.debug("Sample size [%r]", len(rows))

    return [Voice(r) for r in rows]



# TODO: rules
#!!!! rule out dummy rows




fair_voice_chooser = GoodEnough(
    get_items=get_items,
    #?
)
easy_voice_chooser = GoodEnough(
    get_items=get_items,
    #?
)
random_voice_chooser = GoodEnough(
    get_items=get_items,
    #?
)
