import os
import tempfile
from pathlib import Path
from typing import NamedTuple

import pytest


tmp_root = '/tmp'


class FileData(NamedTuple):
    file_path: Path
    file_content: str


def create_file(file_name: str, content: str | None = None) -> FileData:
    dir = Path(tempfile.mkdtemp(dir=tmp_root))
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
