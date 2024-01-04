from base.models import MyBaseModel


class OrderLine(MyBaseModel):
    """Class that represents a purchase of product."""

    id: int
    product_name: str
    ordered_quantity: int
