"""sample_access_tokens

Revision ID: 8fbaade4734b
Revises: 551401a859af
Create Date: 2016-10-16 13:59:59.194491

"""
from alembic import op
import sqlalchemy as sa

from datetime import datetime
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision = '8fbaade4734b'
down_revision = '551401a859af'
branch_labels = None
depends_on = None


access_tokens_table = table(
    'access_tokens',
    column('access_token', sa.String),
    column('user_id', sa.String),
    column('expires_at', sa.DateTime),
    column('issued_at', sa.DateTime)
)

data = [
    {
        'access_token': '100000',
        'expires_at': datetime(1992, 5, 5, 10, 12, 5, 123456),
        'user_id': 'valid_account',
        'issued_at': datetime(1992, 5, 2, 10, 12, 5, 123456),
    },
    {
        'access_token': '100001',
        'expires_at': datetime(2017, 5, 5, 10, 12, 5, 123456),
        'user_id': 'valid_account',
        'issued_at': datetime(1992, 5, 2, 10, 12, 5, 123456),
    },
    {
        'access_token': '100002',
        'expires_at': datetime(2017, 5, 6, 10, 12, 5, 123456),
        'user_id': 'valid_account',
        'issued_at': datetime(1992, 5, 3, 10, 12, 5, 123456),
    },
    {
        'access_token': '200000',
        'expires_at': datetime(1992, 5, 5, 10, 12, 5, 123456),
        'user_id': 'expired_account',
        'issued_at': datetime(1992, 5, 2, 10, 12, 5, 123456),
    },
    {
        'access_token': '200001',
        'expires_at': datetime(2017, 5, 5, 10, 12, 5, 123456),
        'user_id': 'valid_account_1',
        'issued_at': datetime(1992, 5, 2, 10, 12, 5, 123456),
    },
    {
        'access_token': '200002',
        'expires_at': datetime(2017, 5, 6, 10, 12, 5, 123456),
        'user_id': 'valid_account_2',
        'issued_at': datetime(1992, 5, 3, 10, 12, 5, 123456),
    },
]


def upgrade():
    op.bulk_insert(
        access_tokens_table,
        data
    )


def downgrade():
    for row in data:
        op.execute(
            access_tokens_table.delete().where(
                access_tokens_table.c.access_token == row['access_token']
            )
        )

