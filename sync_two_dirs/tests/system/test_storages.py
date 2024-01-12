import tempfile
from pathlib import Path

import pytest

from sync_two_dirs.core.system.storages import SystemFileStorage
from sync_two_dirs.tests.conftest import create_file


@pytest.mark.usefixtures('clean')
class TestSystemFileStorage:
    storage = SystemFileStorage()

    def test_copy(self):
        src_file_path, src_file_content = create_file('file1')
        dst_root = Path(tempfile.mkdtemp())

        self.storage.copy(src_file_path, dst_root)

        dst_file_path = dst_root / src_file_path.name
        assert dst_file_path.exists()
        assert dst_file_path.read_text() == src_file_content

    def test_delete(self):
        dst_file_path, dst_file_content = create_file('file1')

        self.storage.delete(dst_file_path)

        assert not dst_file_path.exists()

    def test_rename(self):
        src_file_path, src_file_content = create_file('file1', 'Some content')
        dst_file_path, dst_file_content = create_file('file3', 'Some content')
        assert src_file_content == dst_file_content

        new_file_path = dst_file_path.parent / src_file_path.name
        self.storage.rename(dst_file_path, new_file_path)

        assert not dst_file_path.exists()
        assert new_file_path.exists()
