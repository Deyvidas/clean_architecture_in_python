import dataclasses
from typing import Any


@dataclasses.dataclass(frozen=True, kw_only=True)
class BaseData:
    def asdict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)
