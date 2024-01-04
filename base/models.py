import uuid

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class MyBaseModel(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex)

    model_config = ConfigDict(
        frozen=True,
    )

    def __hash__(self) -> int:
        return hash((type(self), self.id))

    def __eq__(self, value) -> bool:
        if type(self) is type(value):
            return self.id == value.id
        return False
