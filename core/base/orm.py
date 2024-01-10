from typing import ClassVar

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class BaseOrm(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, nullable=False)

    _show_fields: ClassVar[tuple[str, ...]] = ('id',)

    def __str__(self) -> str:
        class_name = type(self).__name__
        attributes = ', '.join(
            f'{f}={repr(getattr(self, f))}' for f in self._show_fields
        )
        return f'{class_name}({attributes})'

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash((type(self), self.id))

    def __eq__(self, value) -> bool:
        if type(self) is type(value):
            return self.id == value.id
        return False
