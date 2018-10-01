from sqliteutil.base import BaseSqliteUtil


def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


class SqliteSet(BaseSqliteUtil):
    def __init__(self, filename=None, tablename="defaultlist"):
        super().__init__(filename, tablename)

    def append(self, value):
        APPEND = f'INSERT INTO "{self.tablename}" VALUES(?)'
        self.execute(APPEND, (value,))

    def __getitem__(self, item):
        SELECT = f'SELECT value FROM "{self.tablename}" WHERE value=?'
        return self.execute(SELECT, (item,))

    def __contains__(self, item):
        return self[item] is not None

    def remove(self, element):
        if element in self:
            DELETE = f'DELETE FROM "{self.tablename}" WHERE value=?'
            self.execute(DELETE, (element,))
        else:
            raise ValueError(f"Value not in database list.")
