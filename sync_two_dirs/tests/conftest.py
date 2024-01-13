import os
import tempfile
from functools import wraps
from pathlib import Path
from typing import Callable
from typing import Literal
from typing import NamedTuple
from typing import TypeAlias

import pytest


tmp_root = Path('/tmp')


class FileData(NamedTuple):
    file_path: Path
    file_content: str


def create_tmp_dir(root: Path = tmp_root) -> Path:
    dir = Path(tempfile.mkdtemp(dir=root))
    assert dir.exists() and dir.is_dir()
    return dir


def create_file(file_name: str, content: str | None = None) -> FileData:
    dir = create_tmp_dir()
    file_content = f'Content of file ({file_name})'
    if content is not None:
        file_content = content
    file_path = dir / file_name
    file_path.write_text(file_content)

    assert file_path.exists()
    assert file_path.read_text() == file_content

    return FileData(file_path, file_content)


@pytest.fixture(scope='function')
def clean():
    before = os.listdir(tmp_root)
    yield
    after = os.listdir(tmp_root)
    to_delete = set(after) - set(before)
    [os.popen(f'rm -rf {tmp_root}/{d}') for d in to_delete]


Scope: TypeAlias = Literal[
    'function',
    'class',
    'module',
    'package',
    'session',
]


def dependency(depends: list[str] = list(), scope: Scope = 'session'):
    def get_func(func: Callable):
        @wraps(func)
        @pytest.mark.dependency(depends=depends, scope=scope)
        @pytest.mark.order(after=depends)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        return wrapper

    return get_func
