"""sample_real_time

Revision ID: fa89180e982f
Revises: cd163a1b90b4
Create Date: 2016-11-02 23:34:04.198158

"""
from alembic import op
import sqlalchemy as sa



from datetime import datetime
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision = 'fa89180e982f'
down_revision = 'cd163a1b90b4'
branch_labels = None
depends_on = None


real_time_table = table(
    'real_time',
    column('key', sa.String),
    column('user_one_id', sa.String),
    column('user_two_id', sa.String),
    column('latitude_one', sa.Float),
    column('longitude_one', sa.Float),
    column('latitude_two', sa.Float),
    column('longitude_two', sa.Float),
    column('created_at', sa.DateTime),
)


data = [
    {
    	'key': 'abcdefghijklmnopqrstuvwxyz123456',
    	'user_one_id': 'valid_account',
        'user_two_id': 'valid_account_1',
        'latitude_one': 40.741895,
        'longitude_one': -73.989308,
        'latitude_two': 34.052234,
        'longitude_two':  -118.243685,
        'created_at': datetime(1992, 5, 5, 10, 12, 5, 123456),
    },
]


def upgrade():
    op.bulk_insert(
        real_time_table,
        data
    )


def downgrade():
    for row in data:
        op.execute(
            real_time_table.delete().where(
                real_time_table.c.key == row['key']
            )
        )
