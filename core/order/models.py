from pydantic import Field

from core.base.models import MyBaseModel


class OrderLine(MyBaseModel):
    """Class that represents a purchase of product."""

    product_name: str
    ordered_quantity: int = Field(gt=0)
