from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.base.orm import BaseOrm
from core.base.orm import id_uuid


if TYPE_CHECKING:
    from core.batch.orm import BatchOrm


class OrderLineOrm(BaseOrm):
    __tablename__ = 'order_line'

    id: Mapped[id_uuid]
    product_name: Mapped[str] = mapped_column(nullable=False)
    ordered_quantity: Mapped[int] = mapped_column(nullable=False)

    _batch: Mapped['BatchOrm'] = relationship(
        lazy='joined',
        back_populates='_allocations',
    )

    _show_fields = ('id', 'product_name', 'ordered_quantity')
