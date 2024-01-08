from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table

from core.base.orm import metadata
from core.utils.default_factories import get_hex_uuid4


batch = Table(
    'batch',
    metadata,
    Column('id', String(32), primary_key=True, default=get_hex_uuid4),
    Column('product_name', String(255), nullable=False),
    Column('purchased_quantity', Integer, nullable=False),
    Column('estimated_arrival_date', Date, nullable=True),
)


allocation = Table(
    'allocation',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column(
        'order_id',
        ForeignKey('order_line.id', ondelete='CASCADE'),
        nullable=False,
    ),
    Column(
        'batch_id',
        ForeignKey('batch.id', ondelete='CASCADE'),
        nullable=False,
    ),
)
