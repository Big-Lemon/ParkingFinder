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
    column('waiting_user_id', sa.String),
    column('waiting_user_latitude', sa.Float),
    column('waiting_user_longitude', sa.Float),
    column('request_user_id', sa.String),
    column('request_user_latitude', sa.Float),
    column('request_user_longitude', sa.Float),
    column('created_at', sa.DateTime),
)


data = [
    {
    	'waiting_user_id': 'valid_account',
        'waiting_user_latitude': 40.741895,
        'waiting_user_longitude': -73.989308,
        'request_user_id': 'valid_account_1',
        'request_user_latitude': 34.052234,
        'request_user_longitude':  -118.243685,
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
