"""sample_registered_vehicles

Revision ID: 0e3813330b6b
Revises: 27065f41bf8a
Create Date: 2016-10-31 15:57:19.163650

"""
from alembic import op
import sqlalchemy as sa


from datetime import datetime
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision = '0e3813330b6b'
down_revision = '27065f41bf8a'
branch_labels = None
depends_on = None


registered_vehicles_table = table(
    'registered_vehicles',
    column('user_id', sa.String),
    column('plate', sa.String),
)


data = [
    {
    	'user_id': 'valid_account',
        'plate': '6ELA725',
    },
    {
    	'user_id': 'expired_account',
        'plate': '6ELA540',
    },
    {
    	'user_id': 'valid_account_1',
        'plate': '6TRJ224',
    },
    {
    	'user_id': 'valid_account_2',
        'plate': 'ANRCHST',
    },
    {
    	'user_id': 'valid_account_2',
        'plate': '4JTY881',
    },
]


def upgrade():
    op.bulk_insert(
        registered_vehicles_table,
        data
    )


def downgrade():
    for row in data:
        op.execute(
            registered_vehicles_table.delete().where(
                registered_vehicles_table.c.plate == row['plate'] and
                registered_vehicles_table.c.user_id == row['user_id']
            )
        )
