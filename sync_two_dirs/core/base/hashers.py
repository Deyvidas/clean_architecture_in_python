from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import NamedTuple


class Hashes(NamedTuple):
    root: Path
    hashes: dict[str, Path]


class AbstractHasher(ABC):
    @abstractmethod
    def hash_files_in_dir(self, dir_path: Path) -> Hashes:
        raise NotImplementedError

    @abstractmethod
    def hash_file(self, file_path: Path) -> str:
        raise NotImplementedError
