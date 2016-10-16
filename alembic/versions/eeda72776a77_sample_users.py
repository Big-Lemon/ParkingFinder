"""sample users

Revision ID: eeda72776a77
Revises: 83cf2d6876df
Create Date: 2016-10-16 13:59:53.987198

"""
from alembic import op
import sqlalchemy as sa

from datetime import datetime
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision = 'eeda72776a77'
down_revision = '83cf2d6876df'
branch_labels = None
depends_on = None

users_table = table(
    'users',
    column('user_id', sa.String),
    column('first_name', sa.String),
    column('last_name', sa.String),
    column('email', sa.String),
    column('activated_vehicle', sa.String),
    column('created_at', sa.DateTime),
    column('updated_at', sa.DateTime),
)

data = [
    {
        'user_id': 'valid_account',
        'first_name': 'valid',
        'last_name': 'account',
        'email': 'valid_account@gmail.com'
    },
    {
        'user_id': 'expired_account',
        'first_name': 'expired',
        'last_name': 'account',
        'email': 'expired_account@gmail.com',
        'activated_vehicle': '5ZEF241'
    },
    {
        'user_id': 'valid_account_1',
        'first_name': 'valid',
        'last_name': 'account_1',
        'email': 'valid_account_1@gmail.com'
    },
    {
        'user_id': 'valid_account_2',
        'first_name': 'valid',
        'last_name': 'account_2',
        'email': 'valid_account_2@gmail.com',
        'activated_vehicle': '5BFS12A'
    },
]


def upgrade():
    op.bulk_insert(
        users_table,
        data
    )


def downgrade():
    for row in data:
        op.execute(
            table.delete().where(
                table.c.access_token == row['user_id']
            )
        )

