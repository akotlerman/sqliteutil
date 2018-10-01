import random
import sqlite3
import tempfile
from contextlib import contextmanager


class BaseSqliteUtil:
    def __init__(self, filename=None, tablename='basesqliteutil'):
        self.in_temp = filename is None
        if self.in_temp:
            randpart = hex(random.randint(0, 0xffffff))[2:]
            filename = os.path.join(tempfile.gettempdir(), "sqldict" + randpart)

        self.filename = filename
        self.tablename = tablename
        self.conn = self._new_conn()
        MAKE_TABLE = f'CREATE TABLE IF NOT EXISTS "{self.tablename}" (value TEXT PRIMARY KEY)'
        CREATE_INDEX = f'CREATE INDEX IF NOT EXISTS "{self.tablename}Index" ON "{self.tablename}"(value)'
        c = self.conn.cursor()
        c.execute(MAKE_TABLE)
        c.execute(CREATE_INDEX)
        self.conn.commit()

    def __enter__(self):
        if not hasattr(self, "conn") or self.conn is None:
            self.conn = self._new_conn()
        return self

    def __exit__(self, *exc_info):
        self.close()

    def close(self):
        self.conn.close()

    def _new_conn(self):
        return sqlite3.connect(self.filename)

    def __len__(self):
        GET_LEN = f'SELECT COUNT(*) FROM "{self.tablename}"'
        result = self.execute(GET_LEN)
        return result if result is not None else 0

    @contextmanager
    def cursor(self):
        yield self.conn.cursor()
        self.conn.commit()

    def execute(self, sql, parameters=tuple()):
        with self.cursor() as c:
            c.execute(sql, parameters)
            rows = c.fetchone()
            return rows[0] if rows is not None else None

    def __bool__(self):
        SELECT = f'SELECT value FROM "{self.tablename}" LIMIT 1'
        result = self.execute(SELECT)
        return result is not None
