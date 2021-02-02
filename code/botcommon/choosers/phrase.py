import logging

from goodenough import GoodEnough

from botcommon.config import config
from botcommon.db import get_pg_cursor


async def get_items(request):
    from botcommon.models.phrase import Phrase

    percent = min(
        config.CMPDBOT_CHALLENGE_SAMPLE_PHRASE / (await Phrase.count(is_active=True) or 1) * 100,
        100,
    )

    logging.debug("Sample percent [%r]", percent)

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

    logging.debug("Sample size [%r]", len(rows))

    return [Phrase(r) for r in rows]




# TODO: rules...

# slightly demote same author
#!!!! rule out dummy rows




fair_phrase_chooser = GoodEnough(
    get_items=get_items,
    #?
)

easy_phrase_chooser = GoodEnough(
    get_items=get_items,
    #?
)

random_phrase_chooser = GoodEnough(
    get_items=get_items,
    #?
)
