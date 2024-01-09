from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.base.orm import BaseOrm
from core.base.orm import id_int
from core.base.orm import id_uuid


if TYPE_CHECKING:
    from core.order.orm import OrderLineOrm


class BatchOrm(BaseOrm):
    __tablename__ = 'batch'

    id: Mapped[id_uuid]
    product_name: Mapped[str] = mapped_column(nullable=False)
    purchased_quantity: Mapped[int] = mapped_column(nullable=False)
    estimated_arrival_date: Mapped[date] = mapped_column(nullable=True)

    _allocations: Mapped[set['OrderLineOrm']] = relationship(
        lazy='joined',
        back_populates='batch',
        collection_class=set,
    )

    _show_fields = (
        'id',
        'product_name',
        'purchased_quantity',
        'estimated_arrival_date',
    )


class AllocationOrm(BaseOrm):
    __tablename__ = 'allocation'

    id: Mapped[id_int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    order_id: Mapped[str] = mapped_column(
        ForeignKey(column='order_line.id', ondelete='CASCADE'),
        nullable=False,
    )
    batch_id: Mapped[str] = mapped_column(
        ForeignKey(column='batch.id', ondelete='CASCADE'),
        nullable=False,
    )

    _show_fields = ('id', 'order_id', 'batch_id')
