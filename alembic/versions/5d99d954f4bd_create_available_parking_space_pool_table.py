"""create_available_parking_space_table

Revision ID: 5d99d954f4bd
Revises: e6def7ff3050
Create Date: 2016-11-16 07:30:32.785982

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d99d954f4bd'
down_revision = 'e6def7ff3050'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'available_parking_space_pool',
        sa.Column('plate', sa.String(7), sa.ForeignKey('vehicles.plate'), primary_key=True),
        sa.Column('latitude', sa.Float, nullable=False),
        sa.Column('longitude', sa.Float, nullable=False),
        sa.Column('location', sa.String(255), nullable=True),
        sa.Column('level', sa.Integer, nullable=True),
        sa.Column('is_active', sa.Boolean, nullable=False, default=False),
        sa.Column('created_at', sa.DateTime, nullable=False, default=sa.func),
        sa.Column('updated_at', sa.DateTime, nullable=False, default=sa.func),
    )


def downgrade():
    op.drop_table('available_parking_space_pool')
