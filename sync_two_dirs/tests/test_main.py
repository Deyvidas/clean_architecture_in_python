import os
import tempfile
from pathlib import Path

import pytest

from sync_two_dirs.main import determine_actions
from sync_two_dirs.main import sync


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
        source = Path(tempfile.mkdtemp())
        source_file = source / 'useful'
        dest = Path(tempfile.mkdtemp())

        content = 'I\'m very useful file.'
        source_file.write_text(content)

        sync(source, dest)

        expected_path = dest / source_file.name
        assert expected_path.exists()
        assert expected_path.read_text() == content

    def test_when_a_file_has_been_renamed_in_source(self):
        source = Path(tempfile.mkdtemp())
        source_file = source / 'source_file'
        dest = Path(tempfile.mkdtemp())
        dest_file = dest / 'dest_file'

        content = 'I\'m renamed file.'
        source_file.write_text(content)
        dest_file.write_text(content)

        sync(source, dest)

        assert source_file.exists()
        assert not dest_file.exists()

        expected_path = dest / source_file.name
        assert expected_path.exists()
        assert expected_path.read_text() == content

    def test_when_a_file_was_deleted_from_source(self):
        source = Path(tempfile.mkdtemp())
        source_file = source / 'file_to_delete'
        dest = Path(tempfile.mkdtemp())
        dest_file = dest / 'file_to_delete'

        content = 'I\'m file that must be deleted.'
        source_file.write_text(content)
        dest_file.write_text(content)

        while source_file.exists():
            os.remove(str(source_file))

        assert not source_file.exists()
        assert dest_file.exists()

        sync(source, dest)

        assert not dest_file.exists()
