"""add profile pic column to user

Revision ID: afde421ba47b
Revises: 551401a859af
Create Date: 2016-10-21 23:59:33.442956

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'afde421ba47b'
down_revision = '8fbaade4734b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'users',
        sa.Column('profile_picture_url', sa.String(255), nullable=True)
    )


def downgrade():
    op.drop_column(
        'users', 'profile_picture_url'
    )
