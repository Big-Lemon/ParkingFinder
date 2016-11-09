"""sample_check_out_parking_space

Revision ID: 20b77a459069
Revises: a8b4fca89bbc
Create Date: 2016-11-09 08:27:00.540260

"""
from alembic import op
import sqlalchemy as sa

from datetime import datetime
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision = '20b77a459069'
down_revision = 'a8b4fca89bbc'
branch_labels = None
depends_on = None

check_out_parking_space_table = table(
    'check_out_parking_space',
    column('user_id', sa.String),
    column('latitude', sa.Float),
    column('longitude', sa.Float),
    column('created_at', sa.DateTime),
    column('level', sa.Integer),
    column('description', sa.String),
)

data = [
    {
    	'user_id': 'valid_account',
        'latitude': 33.944214,
        'longitude': -118.342667,
        'created_at': datetime(2016, 10, 29, 10, 30, 6, 123456),
        'level': 5,
        'description': "Checkout from parking Lot next to the BurgerKing"
    },
    {
    	'user_id': 'expired_account',
        'latitude': 38.565348,
        'longitude': -121.49231,
        'created_at': datetime(2016, 9, 20, 5, 30, 6, 654321),
        'description': "Checkout from parking space on the Veteran Ave."
    },
    {
    	'user_id': 'valid_account_1',
        'latitude': 32.801128,
        'longitude': -117.240601,
        'created_at': datetime(2016, 10, 16, 6, 15, 2, 321654),
        'level': 2,
        'description': "Checkout from arking Lot 4 in UCSD"
    },
    {
    	'user_id': 'valid_account_2',
        'latitude': 41.533543,
        'longitude': -87.424006,
        'created_at': datetime(2016, 11, 3, 11, 37, 6, 456123)
    },
]


def upgrade():
    for row in data:
        op.bulk_insert(
            check_out_parking_space_table,
            [row]
        )


def downgrade():
    for row in data:
        op.execute(
            check_out_parking_space_table.delete().where(
                check_out_parking_space_table.c.user_id == row['user_id']
            )
        )
