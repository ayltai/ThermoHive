from os import close, remove
from tempfile import mkstemp

from pytest import fixture

from src.data.unix_storage import Storage

@fixture
def temp_storage_file(monkeypatch):
    fd, path = mkstemp()
    close(fd)

    monkeypatch.setattr(Storage, 'FILE_PATH', path)

    yield path
    remove(path)

def test_set_and_get_int(temp_storage_file):
    storage = Storage()
    storage.set_int('foo', 123)

    assert storage.get_int('foo') == 123
    assert storage.get_int('bar') is None

    storage.set_int('bar', 456)

    assert storage.get_int('bar') == 456

    with open(Storage.FILE_PATH) as f:
        lines = f.read().splitlines()

        assert 'foo=123' in lines
        assert 'bar=456' in lines
