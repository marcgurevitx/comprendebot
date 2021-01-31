from Levenshtein import ratio

from botcommon.config import config
from botcommon.model import ModelBase


class Phrase( USE_ModelBase________ ):  # !

    @classmethod
    async def find_similar(cls, conn, normalized_text):
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
    async def insert(cls, conn, *, is_active, original_text, normalized_text=None):
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
