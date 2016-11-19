"""sample_waiting_pool

Revision ID: c6fee4f3dab5
Revises: d88aaa702951
Create Date: 2016-11-19 09:05:07.335218

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime
from sqlalchemy.sql import table, column

# revision identifiers, used by Alembic.
revision = 'c6fee4f3dab5'
down_revision = 'd88aaa702951'
branch_labels = None
depends_on = None

waiting_pool_table = table(
    'waiting_pool',
    column('user_id', sa.String),
    column('latitude', sa.Float),
    column('longitude', sa.Float),
    column('is_active', sa.Boolean),
)

data = [
    {
        'user_id': 'valid_account',
        'latitude': 34.052234,
        'longitude': -118.243685,
        'is_active': True,
    },
    {
        'user_id': 'expired_account',
        'latitude':  34.061386,
        'longitude': -118.433819,
        'is_active': True,
    },
]


def upgrade():
    op.bulk_insert(
        waiting_pool_table,
        data
    )


def downgrade():
    for row in data:
        op.execute(
            waiting_pool_table.delete().where(
                waiting_pool_table.user_id == row['user_id']
            )
        )
