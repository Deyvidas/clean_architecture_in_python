from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.base.orm import BaseOrm


if TYPE_CHECKING:
    from core.batch.orm import BatchOrm


class OrderLineOrm(BaseOrm):
    __tablename__ = 'order_line'

    product_name: Mapped[str] = mapped_column(nullable=False)
    ordered_quantity: Mapped[int] = mapped_column(nullable=False)

    batch_id: Mapped[str] = mapped_column(
        ForeignKey(column='batch.id', ondelete='CASCADE'),
        nullable=True,
    )
    batch: Mapped['BatchOrm'] = relationship(
        lazy='joined',
        back_populates='allocations',
    )

    _show_fields = ('id', 'product_name', 'ordered_quantity')
