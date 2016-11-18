"""parking space pool

Revision ID: bced7c31fc49
Revises: fa89180e982f
Create Date: 2016-11-09 00:28:12.512007

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bced7c31fc49'
down_revision = 'fa89180e982f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'parking_lot',
        sa.Column('plate', sa.String(7), sa.ForeignKey('vehicles.plate'), primary_key=True),
        sa.Column('latitude', sa.DECIMAL(precision=32, scale=6), nullable=False),
        sa.Column('longitude', sa.DECIMAL(precision=32, scale=6), nullable=False),
        sa.Column('location', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, default=sa.func),
        sa.Column('level', sa.Integer, nullable=True),
    )


def downgrade():
    op.drop_table('parking_lot')
