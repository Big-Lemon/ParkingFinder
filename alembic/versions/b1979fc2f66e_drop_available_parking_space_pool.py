"""drop available parking space pool

Revision ID: b1979fc2f66e
Revises: c6fee4f3dab5
Create Date: 2016-11-21 02:09:22.108597

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1979fc2f66e'
down_revision = 'c6fee4f3dab5'
branch_labels = None
depends_on = None

def upgrade():
    op.drop_table('available_parking_space_pool')


def downgrade():
    op.create_table(
        'available_parking_space_pool',
        sa.Column('plate', sa.String(7), sa.ForeignKey('vehicles.plate'), primary_key=True),
        sa.Column('latitude', sa.DECIMAL(precision=32, scale=6), nullable=False),
        sa.Column('longitude', sa.DECIMAL(precision=32, scale=6), nullable=False),
        sa.Column('location', sa.String(255), nullable=True),
        sa.Column('level', sa.Integer, nullable=True),
        sa.Column('is_active', sa.Boolean, nullable=False, default=False),
        sa.Column('created_at', sa.DateTime, nullable=False, default=sa.func),
        sa.Column('updated_at', sa.DateTime, nullable=False, default=sa.func),
    )

