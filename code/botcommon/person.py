from botcommon.db import get_pg_cursor


class Person:

    @classmethod
    async def find(cls, telegram_uid):
        async with get_pg_cursor() as cur:
            await cur.execute(
                """
                    SELECT
                        *
                    FROM
                        person
                    WHERE
                        telegram_uid = %(telegram_uid)s
                    ;
                """,
                locals()
            )
            row = await cur.fetchone()
        if row is not None:
            rv = Person(row)
        else:
            rv = None
        return rv

    @classmethod
    async def insert(cls, **kwargs):
        async with get_pg_cursor() as cur:
            await cur.execute(
                """
                    INSERT INTO person(
                        is_active,
                        telegram_uid,
                        telegram_info,
                        started_ts
                    )
                    VALUES(
                        %(is_active)s,
                        %(telegram_uid)s,
                        %(telegram_info)s,
                        %(started_ts)s
                    )
                    RETURNING *;
                """,
                kwargs
            )
            row = await cur.fetchone()
        return Person(row)

    def __init__(self, row):
        self.row = row
