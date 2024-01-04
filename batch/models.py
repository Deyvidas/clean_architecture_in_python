from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from base.models import MyBaseModel

if TYPE_CHECKING:
    from order.models import OrderLine


class Batch(MyBaseModel):
    """Class that represents a batch of product."""

    product_name: str
    purchased_quantity: int
    estimated_arrival_date: date
    _allocations: set[OrderLine] = set()

    @property
    def allocations(self) -> set[OrderLine]:
        return self._allocations

    @property
    def allocated_quantity(self) -> int:
        return sum(a.ordered_quantity for a in self.allocations)

    @property
    def available_quantity(self) -> int:
        return self.purchased_quantity - self.allocated_quantity

    def allocate(self, order: OrderLine) -> None:
        """Add order to the allocations set."""
        if self.can_allocate(order):
            self._allocations.add(order)
        # TODO WHAT MUST BE IF THE ORDER CAN'T BE ALLOCATED?

    def can_allocate(self, order: OrderLine) -> bool:
        """Verify if:
        - the quantity ordered can be allocated from this batch;
        - the product_name in order coincide with product_name in Batch.
        """
        return (
            self.product_name == order.product_name
            and self.available_quantity >= order.ordered_quantity
        )

    def deallocate(self, order: OrderLine) -> None:
        """Remove order from the allocations set."""
        if order not in self.allocations:
            return
        self.allocations.remove(order)
