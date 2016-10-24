"""change size of activated_vehicle in user table

Revision ID: 4ca264391f2f
Revises: cacd3d831ce7
Create Date: 2016-10-22 20:17:24.424623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ca264391f2f'
down_revision = 'cacd3d831ce7'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column(
        'users', 'activated_vehicle'
    )
    op.add_column(
        'users',
        sa.Column('activated_vehicle', sa.String(7), nullable=True)
    )


def downgrade():
    op.drop_column(
        'users', 'activated_vehicle'
    )
    op.add_column(
        'users',
        sa.Column('activated_vehicle', sa.String(8), nullable=True)
    )

