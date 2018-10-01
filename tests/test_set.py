from pathlib import Path

import pytest

from sqliteutil.sqliteset import SqliteSet, is_int


def test_list_functionality():
    dbfile = Path('sample.sqlite')
    if dbfile.exists():
        dbfile.unlink()
    with SqliteSet(str(dbfile)) as db:
        assert not db
        assert len(db) == 0
        db.append('value here')
        assert db
        assert len(db) == 1
        assert db['value here'] == 'value here'
        assert db['no value here'] is None
        assert 'value here' in db
        with pytest.raises(ValueError):
            db.remove('invalid value')

        for i in range(100):
            db.append(f"value{i}")
        assert len(db) == 101

        db.remove("value50")
        assert len(db) == 100

        db.remove("value20")
        assert len(db) == 99

    with SqliteSet(str(dbfile)) as db:
        db.remove("value1")
        assert len(db) == 98



def test_is_int():
    assert is_int(10)
    assert not is_int('blah')
    assert is_int("100")
