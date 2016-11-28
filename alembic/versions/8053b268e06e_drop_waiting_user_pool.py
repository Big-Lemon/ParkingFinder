"""drop waiting user pool

Revision ID: 8053b268e06e
Revises: b1979fc2f66e
Create Date: 2016-11-21 02:10:31.714951

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8053b268e06e'
down_revision = 'b1979fc2f66e'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('waiting_pool')


def downgrade():
    op.create_table(
        'waiting_pool',
        sa.Column('user_id', sa.String(64), sa.ForeignKey('users.user_id'), nullable=False),
        sa.Column('longitude', sa.DECIMAL(precision=32, scale=6), nullable=False),
        sa.Column('latitude', sa.DECIMAL(precision=32, scale=6), nullable=False),
        sa.Column('location', sa.String(255), nullable=True),
        sa.Column('level', sa.Integer, nullable=True),
        sa.Column('is_active', sa.Boolean, nullable=False, default=False),
        sa.Column('created_at', sa.DateTime, nullable=False, default=sa.func),
    )
