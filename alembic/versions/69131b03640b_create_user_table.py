"""create user table

Revision ID: 69131b03640b
Revises: 
Create Date: 2016-10-08 18:57:56.455709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69131b03640b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('user_id', sa.String(64), primary_key=True, autoincrement=False),
        sa.Column('first_name', sa.String(32), nullable=False),
        sa.Column('last_name', sa.String(32), nullable=False),
        sa.Column('activated_vehicle', sa.String(7), nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=True, default=sa.func),
        sa.Column('updated_at', sa.DateTime, nullable=True, default=sa.func),
        sa.Column('profile_picture_url', sa.String(255), nullable=True)
    )


def downgrade():
    op.drop_table('users')


