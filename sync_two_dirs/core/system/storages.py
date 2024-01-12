import os
from pathlib import Path
from typing import override

from sync_two_dirs.core.base.storages import AbstractFileStorage


class SystemFileStorage(AbstractFileStorage):
    @override
    def copy(self, file_path: Path, into_dir_path: Path) -> None:
        command = command = f'cp {file_path} {into_dir_path}'
        while not (into_dir_path / file_path.name).exists():
            os.popen(command)

    @override
    def delete(self, file_path: Path) -> None:
        command = f'rm {file_path}'
        while file_path.exists():
            os.popen(command)

    @override
    def rename(self, old_path: Path, new_path: Path):
        command = f'mv {old_path} {new_path}'
        while not new_path.exists():
            os.popen(command)
