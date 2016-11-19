"""sample_matched_parking_space_list

Revision ID: 4293326845b2
Revises: 5d99d954f4bd
Create Date: 2016-11-17 05:58:36.428820

"""
from alembic import op
import sqlalchemy as sa

from datetime import datetime
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision = '4293326845b2'
down_revision = '5d99d954f4bd'
branch_labels = None
depends_on = None

matched_parking_space_list_table = table(
    'matched_parking_space_list',
    column('user_id', sa.String),
    column('plate', sa.String),
    # column('status', sa.String),
    column('status', sa.Enum('awaiting', 'rejected', 'accepted', 'expired', name='status_types')),
    column('created_at', sa.DateTime),
)

data = [
    {
        'user_id': 'valid_account',
        'plate': '6ELA725',
        'status': 'awaiting',
        'created_at': datetime(2016, 11, 12, 10, 15, 5, 123456),
    },
    {
        'user_id': 'valid_account_1',
        'plate': '6TRJ224',
        'status': 'rejected',
        'created_at': datetime(2016, 11, 14, 10, 12, 5, 123456),
    },
    {
        'user_id': 'valid_account_2',
        'plate': 'ANRCHST',
        'status': 'awaiting',
        'created_at': datetime(2016, 11, 15, 10, 12, 5, 123456),
    },
    {
        'user_id': 'valid_account_2',
        'plate': '4JTY881',
        'status': 'awaiting',
        'created_at': datetime(2016, 11, 16, 9, 12, 5, 123456),
    },
    {
        'user_id': 'expired_account',
        'plate': '6ELA540',
        'status': 'expired',
        'created_at': datetime(2016, 11, 16, 10, 12, 5, 123456),
    },
]


def upgrade():
    for row in data:
        op.bulk_insert(
            matched_parking_space_list_table,
            [row]
        )


def downgrade():
    for row in data:
        op.execute(
            matched_parking_space_list_table.delete().where(
                matched_parking_space_list_table.c.plate == row['plate']
            )
        )