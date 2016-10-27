"""sample_users_

Revision ID: 551401a859af
Revises: eeda72776a77
Create Date: 2016-10-22 18:01:00.381843

"""

from alembic import op
import sqlalchemy as sa

from datetime import datetime
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision = '551401a859af'
down_revision = 'eeda72776a77'
branch_labels = None
depends_on = None


users_table = table(
    'users',
    column('user_id', sa.String),
    column('first_name', sa.String),
    column('last_name', sa.String),
    column('activated_vehicle', sa.String),
    column('created_at', sa.DateTime),
    column('updated_at', sa.DateTime),
    column('profile_picture_url', sa.String),
)

data = [
    {
        'user_id': 'valid_account',
        'first_name': 'valid',
        'last_name': 'account',
        'created_at': datetime(1992, 5, 2, 10, 12, 5, 123456),
        'profile_picture_url': 'www.123.com'

    },
    {
        'user_id': 'expired_account',
        'first_name': 'expired',
        'last_name': 'account',
        'activated_vehicle': '5ZEF241'
    },
    {
        'user_id': 'valid_account_1',
        'first_name': 'valid',
        'last_name': 'account_1',
    },
    {
        'user_id': 'valid_account_2',
        'first_name': 'valid',
        'last_name': 'account_2',
        'activated_vehicle': '5BFS12A'
    },
]


def upgrade():
    for row in data:
        op.bulk_insert(
            users_table,
            [row]
        )


def downgrade():
    for row in data:
        op.execute(
            table.delete().where(
                table.c.access_token == row['user_id']
            )
        )

