"""create_vehicle_table_

Revision ID: eeda72776a77
Revises: 83cf2d6876df
Create Date: 2016-10-16 13:59:53.987198

"""
from alembic import op
import sqlalchemy as sa

from datetime import datetime
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision = 'eeda72776a77'
down_revision = '83cf2d6876df'
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

