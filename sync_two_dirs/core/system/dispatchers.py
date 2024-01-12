from dataclasses import dataclass
from pathlib import Path
from typing import override

from sync_two_dirs.core.base.dispatchers import AbstractDispatcher
from sync_two_dirs.core.base.hashers import AbstractHasher
from sync_two_dirs.core.base.hashers import Hashes
from sync_two_dirs.core.base.storages import AbstractFileStorage


@dataclass
class SystemDispatcher(AbstractDispatcher):
    hasher: AbstractHasher
    storage: AbstractFileStorage

    @override
    def synchronize(self, src_root: Path, dst_root: Path):
        src_hashes = self.hasher.hash_files_in_dir(src_root)
        dst_hashes = self.hasher.hash_files_in_dir(dst_root)

        actions = self.determine_actions(
            src_hashes=src_hashes,
            dst_hashes=dst_hashes,
        )

        [function(*args) for function, *args in actions]

    @override
    def determine_actions(self, src_hashes: Hashes, dst_hashes: Hashes):
        for src_hash, src_path in src_hashes.hashes.items():
            # If the file is not in the destination directory.
            if dst_hashes.hashes.get(src_hash, None) is None:
                yield (self.storage.copy, src_path, dst_hashes.root)

            # If the file is in the destination directory but has a different name.
            elif (dp := dst_hashes.hashes[src_hash]).name != src_path.name:
                yield (self.storage.rename, dp, dp.parent / src_path.name)

        # If the file is in the destination directory but not in the source directory.
        extra_hashes = set(dst_hashes.hashes) - set(src_hashes.hashes)
        for hash in extra_hashes:
            yield (self.storage.delete, dst_hashes.hashes[hash])
