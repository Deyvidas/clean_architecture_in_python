from pydantic import BaseModel
from pydantic import ConfigDict


class MyBaseModel(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )
