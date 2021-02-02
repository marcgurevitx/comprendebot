from Levenshtein import ratio

from botcommon.config import config
from botcommon.choosers.phrase import (
    fair_phrase_chooser,
    easy_phrase_chooser,
    random_phrase_chooser,
)
from botcommon.modelbase import ModelBase


class Phrase(ModelBase):

    @classmethod
    async def choose_fair(cls, person_n_prev_success, exclude_phrases):
        return await fair_phrase_chooser.async_pick({
            "person_n_prev_success": person_n_prev_success,
            "exclude_phrases": [p.row.id for p in exclude_phrases],
        })

    @classmethod
    async def choose_easy(cls, exclude_phrases):
        return await easy_phrase_chooser.async_pick({
            "exclude_phrases": [p.row.id for p in exclude_phrases],
        })

    @classmethod
    async def choose_random(cls, exclude_phrases):
        return await random_phrase_chooser.async_pick({
            "exclude_phrases": [p.row.id for p in exclude_phrases],
        })




    @classmethod
    async def xxxxx_find_similar(cls, conn, normalized_text):
        similar = []

        async with conn.cursor() as cur:
            await cur.execute(
                """
                    SELECT
                        *
                    FROM
                        phrase
                    ;
                """,
            )
            async for row in cur:
                rat = ratio(normalized_text, row.normalized_text)
                if rat >= config.CMPDBOT_SIMILARITY_RATIO:
                    similar.append([rat, row])

        return similar

    @classmethod
    async def xxxxx_insert(cls, conn, *, is_active, original_text, normalized_text=None):
        async with conn.cursor() as cur:
            await cur.execute(
                """
                    INSERT INTO phrase (
                        is_active,
                        original_text,
                        normalized_text
                    )
                    VALUES
                        (
                            %(is_active)s,
                            %(original_text)s,
                            %(normalized_text)s
                        )
                    ;
                """,
                locals()
            )
