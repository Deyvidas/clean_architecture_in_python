from base import metadata
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table

from core.utils.default_factories import get_hex_uuid4


order_line = Table(
    'order_line',
    metadata,
    Column('id', String(32), primary_key=True, default=get_hex_uuid4),
    Column('product_name', String(255), nullable=False),
    Column('ordered_quantity', Integer, nullable=False),
)
