from abc import ABC
from abc import abstractmethod
from pathlib import Path

from sync_two_dirs.core.base.hashers import Hashes


class AbstractDispatcher(ABC):
    @abstractmethod
    def synchronize(self, src_root: Path, dst_root: Path):
        raise NotImplementedError

    @abstractmethod
    def determine_actions(self, src_hashes: Hashes, dst_hashes: Hashes):
        raise NotImplementedError
