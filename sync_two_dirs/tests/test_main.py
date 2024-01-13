from pathlib import Path

import pytest

from sync_two_dirs.main import determine_actions
from sync_two_dirs.main import sync
from sync_two_dirs.tests.conftest import create_file
from sync_two_dirs.tests.conftest import create_tmp_dir


src_root = Path('/src')
dst_root = Path('/dst')


class TestDetermineActions:
    def test_when_a_file_has_added_in_source(self):
        src_hashes = {'hash1': src_root / 'file'}
        dst_hashes = {}

        actions = determine_actions(
            src_hashes=src_hashes,
            dst_hashes=dst_hashes,
            src_root=src_root,
            dst_root=dst_root,
        )

        assert list(actions) == [('COPY', src_hashes['hash1'], dst_root)]

    def test_when_a_file_has_been_renamed_in_source(self):
        src_hashes = {'hash1': src_root / 'new_name'}
        dst_hashes = {'hash1': dst_root / 'old_name'}

        actions = determine_actions(
            src_hashes=src_hashes,
            dst_hashes=dst_hashes,
            src_root=src_root,
            dst_root=dst_root,
        )

        assert list(actions) == [
            (
                'RENAME',
                dst_hashes['hash1'],
                dst_root / src_hashes['hash1'].name,
            )
        ]

    def test_when_a_file_was_deleted_from_source(self):
        src_hashes = {}
        dst_hashes = {'hash1': dst_root / 'file'}

        actions = determine_actions(
            src_hashes=src_hashes,
            dst_hashes=dst_hashes,
            src_root=src_root,
            dst_root=dst_root,
        )

        assert list(actions) == [('DELETE', dst_hashes['hash1'])]


@pytest.mark.usefixtures('clean')
class TestSyncFunction:
    def test_when_a_file_has_added_in_source(self):
        src_file_path, src_content = create_file('useful', 'I\'m useful file.')
        dst_root = create_tmp_dir()

        sync(src_file_path.parent, dst_root)

        expected_path = dst_root / src_file_path.name
        assert expected_path.exists()
        assert expected_path.read_text() == src_content

    def test_when_a_file_has_been_renamed_in_source(self):
        content = 'I\'m renamed file.'
        src_file_path, src_content = create_file('renamed_file', content)
        dst_file_path, _ = create_file('original_file', content)

        sync(src_file_path.parent, dst_file_path.parent)

        assert src_file_path.exists()
        assert not dst_file_path.exists()

        expected_path = dst_file_path.parent / src_file_path.name
        assert expected_path.exists()
        assert expected_path.read_text() == src_content

    def test_when_a_file_was_deleted_from_source(self):
        content = 'I\'m file that must be deleted.'
        src_root = create_tmp_dir()
        dst_file_path, dst_content = create_file('file_to_delete', content)

        assert not (src_root / dst_file_path.name).exists()
        assert dst_file_path.exists()

        sync(src_root, dst_file_path.parent)

        assert not dst_file_path.exists()
