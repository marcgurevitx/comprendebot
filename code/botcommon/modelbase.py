from botcommon.db import get_pg_cursor


class ModelBase:
    table_name = None

    @classmethod
    def get_table_name(cls):
        return cls.table_name or cls.__name__.lower()

    @classmethod
    def sql_where(cls, keys):
        return " ".join(f"AND {k} = %({k})s" for k in keys)

    @classmethod
    def sql_columns(cls, keys):
        return ", ".join(keys)

    @classmethod
    def sql_values(cls, keys):
        return ", ".join(f"%({k})s" for k in keys)

    @classmethod
    def sql_set(cls, keys):
        return ", ".join(f"{k} = %({k})s" for k in keys)

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
        async with get_pg_cursor() as cur:
            await cur.execute(
                f"""
                    SELECT
                        *
                    FROM
                        {cls.get_table_name()}
                    WHERE
                        1 = 1 {cls.sql_where(kwargs)}
                    ;
                """,
                kwargs,
            )
            return await (getattr(cur, fetch_method))()

    @classmethod
    async def select_sql_one(cls, sql, **kwargs):
        row = await cls._select_sql("fetchone", sql, **kwargs)
        if row:
            return cls(row)

    @classmethod
    async def select_sql_all(cls, sql, **kwargs):
        rows = await cls._select_sql("fetchall", sql, **kwargs)
        return [cls(r) for r in rows]

    @classmethod
    async def _select_sql(cls, fetch_method, sql, **kwargs):
        async with get_pg_cursor() as cur:
            await cur.execute(sql, kwargs)
            return await (getattr(cur, fetch_method))()

    @classmethod
    async def count(cls, **kwargs):
        async with get_pg_cursor() as cur:
            await cur.execute(
                f"""
                    SELECT
                        COUNT(*) as nrows
                    FROM
                        {cls.get_table_name()}
                    WHERE
                        1 = 1 {cls.sql_where(kwargs)}
                    ;
                """,
                kwargs,
            )
            row = await cur.fetchone()
            return row.nrows

    @classmethod
    async def select_random(cls, limit, /, **kwargs):
        percent = min(
            limit / (await cls.count(**kwargs) or 1) * 100,
            100,
        )
        async with get_pg_cursor() as cur:
            await cur.execute(
                f"""
                    SELECT
                        *
                    FROM
                        {cls.get_table_name()} TABLESAMPLE BERNOULLI ({percent})
                    WHERE
                        1 = 1 {cls.sql_where(kwargs)}
                    ;
                """,
                kwargs,
            )
            rows = await cur.fetchall()
        return [cls(r) for r in rows]

    @classmethod
    async def insert(cls, **kwargs):
        async with get_pg_cursor() as cur:
            await cur.execute(
                f"""
                    INSERT INTO {cls.get_table_name()}(
                        {cls.sql_columns(kwargs)}
                    )
                    VALUES(
                        {cls.sql_values(kwargs)}
                    )
                    RETURNING *;
                """,
                kwargs,
            )
            row = await cur.fetchone()
        return cls(row)

    @classmethod
    async def delete(cls, **kwargs):
        async with get_pg_cursor() as cur:
            await cur.execute(
                f"""
                    DELETE FROM
                        {cls.get_table_name()}
                    WHERE
                        1 = 1 {cls.sql_where(kwargs)}
                    ;
                """,
                kwargs,
            )

    def __init__(self, row):
        self.row = row

    async def update(self, **kwargs):
        assert kwargs
        assert "id" not in kwargs
        async with get_pg_cursor() as cur:
            await cur.execute(
                f"""
                    UPDATE {self.get_table_name()}
                    SET
                        {self.sql_set(kwargs)}
                    WHERE
                        id = %(id)s
                    RETURNING *;
                """,
                {**kwargs, "id": self.row.id},
            )
            self.row = await cur.fetchone()
