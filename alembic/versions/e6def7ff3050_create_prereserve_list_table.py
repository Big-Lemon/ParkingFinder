"""create prereserve list table

Revision ID: e6def7ff3050
Revises: 7d7502ffee48
Create Date: 2016-11-09 00:34:51.177051

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6def7ff3050'
down_revision = '7d7502ffee48'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'prereserved_list',
        sa.Column('user_id', sa.String(64), sa.ForeignKey('users.user_id'), nullable=False),
        # TODO add foreign key constraint (ParkingSpace.id)
        sa.Column('parking_id', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, default=sa.func),
        sa.Column('updated_at', sa.DateTime, nullable=False, default=sa.func),
    )


def downgrade():
    op.drop_table('prereserved_list')

