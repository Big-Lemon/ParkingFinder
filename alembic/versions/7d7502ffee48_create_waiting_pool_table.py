"""waiting pool

Revision ID: 7d7502ffee48
Revises: bced7c31fc49
Create Date: 2016-11-09 00:33:32.326960

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d7502ffee48'
down_revision = 'bced7c31fc49'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'waiting_pool',
        sa.Column('user_id', sa.String(64), sa.ForeignKey('users.user_id'), nullable=False),
        sa.Column('longitude', sa.Float, nullable=False),
        sa.Column('latitude', sa.Float, nullable=False),
        sa.Column('location', sa.String(255), nullable=True),
        sa.Column('level', sa.Integer, nullable=True),
        sa.Column('is_active', sa.Boolean, nullable=False, default=False),
        sa.Column('created_at', sa.DateTime, nullable=False, default=sa.func),
    )


def downgrade():
    op.drop_table('waiting_pool')


