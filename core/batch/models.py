from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING
from typing import Self

from pydantic import Field
from pydantic import computed_field

from core.base.models import MyBaseModel
from core.utils.exceptions import OutOfStock


if TYPE_CHECKING:
    from core.order.models import OrderLine


class Batch(MyBaseModel):
    """Class that represents a batch of product."""

    product_name: str
    purchased_quantity: int
    estimated_arrival_date: date | None = Field(default=None)
    _allocations: list[OrderLine] = list()

    def __gt__(self, other: Self) -> bool:
        # TODO WHAT MUST BE IF self.ead == other.ead == None.
        if self.estimated_arrival_date is None:
            return False
        elif other.estimated_arrival_date is None:
            return True
        return self.estimated_arrival_date > other.estimated_arrival_date

    @computed_field  # type: ignore[misc]
    @property
    def allocations(self) -> list[OrderLine]:
        return self._allocations

    @property
    def allocated_quantity(self) -> int:
        return sum(a.ordered_quantity for a in self.allocations)

    @property
    def available_quantity(self) -> int:
        return self.purchased_quantity - self.allocated_quantity

    def allocate(self, order: OrderLine) -> None:
        """Add order to the allocations list."""
        if not self.can_allocate(order):
            return  # TODO WHAT MUST BE IF THE ORDER CAN'T BE ALLOCATED?

        try:
            self._allocations.pop(self.allocations.index(order))
        except ValueError:
            pass
        finally:
            self._allocations.append(order)

    def can_allocate(self, order: OrderLine) -> bool:
        """Verify if:
        - the quantity ordered can be allocated from this batch;
        - the product_name in order coincide with product_name in Batch.
        """
        if self.product_name != order.product_name:
            return False
        if self.available_quantity < order.ordered_quantity:
            return False
        return True

    def deallocate(self, order: OrderLine) -> None:
        """Remove order from the allocated orders set."""
        if order in self.allocations:
            self.allocations.remove(order)
        # TODO WHAT MUST BE IF THE ORDER CAN'T BE DEALLOCATED?


def allocate(order: OrderLine, batches: list[Batch]) -> str:
    """A certain quantity of product from an earlier batch is reserved for order.

    Args:
        order (OrderLine): The client order.
        batches (list[Batch]): The list of batches that satisfy the order.

    Returns:
        str: An UUID for the most recent batch that satisfied the order.
    """
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(order))
    except StopIteration:
        raise OutOfStock(f'{order.product_name}')

    batch.allocate(order)
    return batch.id
