from abc import ABC
from abc import abstractmethod
from pathlib import Path


class AbstractFileStorage(ABC):
    @abstractmethod
    def copy(self, file_path: Path, into_dir_path: Path) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, file_path: Path) -> None:
        raise NotImplementedError

    @abstractmethod
    def rename(self, old_path: Path, new_path: Path) -> None:
        raise NotImplementedError
