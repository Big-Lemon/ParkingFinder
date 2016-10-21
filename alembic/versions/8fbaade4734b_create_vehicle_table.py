"""create_vehicle_table

Revision ID: 8fbaade4734b
Revises: 551401a859af
Create Date: 2016-10-22 18:01:00.381843

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8fbaade4734b'
down_revision = '551401a859af'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'vehicles',
        sa.Column('plate', sa.String(7), primary_key=True),
        sa.Column('brand', sa.String(32), nullable=False),
        sa.Column('model', sa.String(32), nullable=False),
        sa.Column('color', sa.String(32), nullable=False),
        sa.Column('year', sa.Integer, nullable=False),
    )


def downgrade():
    op.drop_table('vehicles')
