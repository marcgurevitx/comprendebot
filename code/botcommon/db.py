import threading  # for lock

from aiopg import create_pool
from psycopg2.extras import NamedTupleCursor

from botcommon.config import config

_lock = threading.Lock()
_pool = None


async def get_pg_pool():
    global _pool

    with _lock:
        if _pool is None:
            _pool = await create_pool(
                host=config.POSTGRES_HOST,
                port=config.POSTGRES_PORT,
                user=config.POSTGRES_USER,
                password=config.POSTGRES_PASSWORD,
                dbname=config.POSTGRES_DB,
                cursor_factory=NamedTupleCursor,
            )

    return _pool
