import hashlib
from pathlib import Path
from typing import override

from sync_two_dirs.core.base.hashers import AbstractHasher
from sync_two_dirs.core.base.hashers import Hashes


class BaseHasher(AbstractHasher):
    @override
    def hash_files_in_dir(self, dir_path: Path) -> Hashes:
        hashes = dict()
        for root, _, files in dir_path.walk():
            for file in files:
                file_path = root / file
                hashes[self.hash_file(file_path)] = file_path
        return Hashes(root=dir_path, hashes=hashes)


class SystemHasherSHA1(BaseHasher):
    @override
    def hash_file(self, file_path: Path) -> str:
        hasher = hashlib.sha1()
        with file_path.open('rb') as file:
            hasher.update(file.read())
        return hasher.hexdigest()
