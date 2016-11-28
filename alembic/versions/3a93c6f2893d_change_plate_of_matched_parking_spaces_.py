"""change plate of matched parking spaces to primary key

Revision ID: 3a93c6f2893d
Revises: 77fd8f39954d
Create Date: 2016-11-25 02:48:02.497215

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a93c6f2893d'
down_revision = '77fd8f39954d'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'matched_parking_space_list',
        column_name='plate',
        primary_key=True,
        existing_type=sa.String(7)
    )


def downgrade():
    op.alter_column(
        'matched_parking_space_list',
        column_name='plate',
        primary_key=False,
        existing_type=sa.String(7)
    )

