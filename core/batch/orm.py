from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.base.orm import BaseOrm


if TYPE_CHECKING:
    from core.order.orm import OrderLineOrm


class BatchOrm(BaseOrm):
    __tablename__ = 'batch'

    product_name: Mapped[str] = mapped_column(nullable=False)
    purchased_quantity: Mapped[int] = mapped_column(nullable=False)
    estimated_arrival_date: Mapped[date] = mapped_column(nullable=True)

    allocations: Mapped[list['OrderLineOrm']] = relationship(
        lazy='joined',
        back_populates='batch',
    )

    _show_fields = (
        'id',
        'product_name',
        'purchased_quantity',
        'estimated_arrival_date',
    )
