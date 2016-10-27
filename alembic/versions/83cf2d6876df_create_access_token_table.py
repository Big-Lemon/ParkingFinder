"""create access token table

Revision ID: 83cf2d6876df
Revises: 69131b03640b
Create Date: 2016-10-09 16:02:23.401746

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83cf2d6876df'
down_revision = '69131b03640b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'access_tokens',
        sa.Column('access_token', sa.String(255), primary_key=True),
        sa.Column('user_id', sa.String(64), sa.ForeignKey('users.user_id'), index=True),
        sa.Column('expires_at', sa.DateTime, nullable=False),
        sa.Column('issued_at', sa.DateTime, nullable=False)
    )


def downgrade():
    op.drop_table('access_tokens')


