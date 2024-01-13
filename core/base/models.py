from typing import Annotated

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from core.utils.default_factories import get_hex_uuid4


uuid = Annotated[str, Field(pattern=r'^[0-9a-z]{32}$', validate_default=True)]


class MyBaseModel(BaseModel):
    id: uuid = Field(default_factory=get_hex_uuid4)

    model_config = ConfigDict(
        frozen=True,
        from_attributes=True,
        extra='allow',
    )

    def __hash__(self) -> int:
        return hash((type(self), self.id))

    def __eq__(self, value) -> bool:
        if type(self) is type(value):
            return self.id == value.id
        return False
