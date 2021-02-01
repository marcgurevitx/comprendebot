from botcommon.db import get_pg_cursor


class ModelBase:
    table_name = None

    @classmethod
    def get_table_name(cls):
        return cls.table_name or cls.__name__.lower()

    @classmethod
    async def select_one(cls, **kwargs):
        row = await cls._select("fetchone", **kwargs)
        if row:
            return cls(row)

    @classmethod
    async def select_all(cls, **kwargs):
        rows = await cls._select("fetchall", **kwargs)
        return [cls(r) for r in rows]

    @classmethod
    async def _select(cls, fetch_method, **kwargs):
        sql_where = " ".join(
            f"AND {k} = %({k})s"
            for k
            in kwargs
        )
        async with get_pg_cursor() as cur:
            await cur.execute(
                f"""
                    SELECT
                        *
                    FROM
                        {cls.get_table_name()}
                    WHERE
                        1 = 1 {sql_where}
                    ;
                """,
                kwargs,
            )
            return await (getattr(cur, fetch_method))()

    @classmethod
    async def count(cls, **kwargs):
        sql_where = " ".join(
            f"AND {k} = %({k})s"
            for k
            in kwargs
        )
        async with get_pg_cursor() as cur:
            await cur.execute(
                f"""
                    SELECT
                        COUNT(*) as nrows
                    FROM
                        {cls.get_table_name()}
                    WHERE
                        1 = 1 {sql_where}
                    ;
                """,
                kwargs,
            )
            row = await cur.fetchone()
            return row.nrows

    @classmethod
    async def insert(cls, **kwargs):
        sql_columns = ", ".join(kwargs)
        sql_values = ", ".join(
            f"%({k})s"
            for k
            in kwargs
        )
        async with get_pg_cursor() as cur:
            await cur.execute(
                f"""
                    INSERT INTO {cls.get_table_name()}(
                        {sql_columns}
                    )
                    VALUES(
                        {sql_values}
                    )
                    RETURNING *;
                """,
                kwargs
            )
            row = await cur.fetchone()
        return cls(row)

    def __init__(self, row):
        self.row = row
