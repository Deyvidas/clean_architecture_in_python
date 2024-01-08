from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from utils.default_factories import get_hex_uuid4


class MyBaseModel(BaseModel):
    id: str = Field(default_factory=get_hex_uuid4)

    model_config = ConfigDict(
        frozen=True,
    )

    def __hash__(self) -> int:
        return hash((type(self), self.id))

    def __eq__(self, value) -> bool:
        if type(self) is type(value):
            return self.id == value.id
        return False
