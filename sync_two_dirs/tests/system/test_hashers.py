import hashlib

import pytest

from sync_two_dirs.core.base.hashers import Hashes
from sync_two_dirs.core.system.hashers import SystemHasherSHA1
from sync_two_dirs.tests.conftest import create_file


@pytest.mark.usefixtures('clean')
class TestHasherSHA1:
    hasher = SystemHasherSHA1()

    def test_single_file(self):
        file_path, file_content = create_file('file1')

        returned_hash = self.hasher.hash_file(file_path)
        estimated_hash = hashlib.sha1(file_content.encode()).hexdigest()
        assert returned_hash == estimated_hash

    def test_directory(self):
        file1_path, file1_content = create_file('file1')
        file2_path, file2_content = create_file('file2')
        main_dir = file1_path.parent
        file2_path = file2_path.rename(main_dir / file2_path.name)

        returned_result = self.hasher.hash_files_in_dir(main_dir)
        file1_hash = hashlib.sha1(file1_content.encode()).hexdigest()
        file2_hash = hashlib.sha1(file2_content.encode()).hexdigest()
        estimated_result = Hashes(
            root=main_dir,
            hashes={
                file1_hash: file1_path,
                file2_hash: file2_path,
            },
        )
        assert returned_result == estimated_result
