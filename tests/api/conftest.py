from enum import Enum
from typing import Callable
from typing import TypeAlias

from fastapi import Response
from fastapi.testclient import TestClient

from api.v1.root import api_v1


CLIENT = TestClient(api_v1)
CL_METHODS: TypeAlias = Callable[..., Response]


class Client(Enum):
    get = CLIENT.get
    post = CLIENT.post
    put = CLIENT.put
    patch = CLIENT.patch
    delete = CLIENT.delete
    head = CLIENT.head
    options = CLIENT.options

    def __call__(self, *args, **kwargs):
        return self.value
