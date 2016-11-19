"""sample_parking_lot

Revision ID: d88aaa702951
Revises: 5d99d954f4bd
Create Date: 2016-11-17 04:47:16.786789

"""
from alembic import op
import sqlalchemy as sa

from datetime import datetime
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision = 'd88aaa702951'
down_revision = '4293326845b2'
branch_labels = None
depends_on = None


parking_lot_table = table(
    'parking_lot',
    column('plate', sa.String),
    column('latitude', sa.Float),
    column('longitude', sa.Float),
    column('location', sa.String),
    column('created_at', sa.DateTime),
    column('level', sa.Integer),
)

data = [
    {
        'plate': '4JTY881',
        'latitude': 34.052234, 
        'longitude': -118.243685,
        'location': 'los angeles',
        'created_at': datetime(2016, 11, 16, 10, 12, 5, 123456),
        'level': 3,
    },
    {
        'plate': '6ELA540',
        'latitude': 34.061386, 
        'longitude': -118.433819, 
        'location': 'UCLA',
        'created_at': datetime(2016, 11, 15, 10, 12, 5, 123456),
        'level': 1,
    },
]


def upgrade():
	for row in data:
		op.bulk_insert(
			parking_lot_table,
			[row]
        )    


def downgrade():
    pass
