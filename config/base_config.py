from pydantic import BaseModel
from pydantic import ConfigDict


class BaseConfig(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        frozen=True,
    )
