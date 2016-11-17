"""create matched parking space list table

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
        'matched_parking_space_list',
        sa.Column('user_id', sa.String(64), sa.ForeignKey('users.user_id'), nullable=False),
        sa.Column('plate', sa.String(7), sa.ForeignKey('vehicles.plate'), nullable=False),
        sa.Column('status', sa.Enum('awaiting', 'rejected', 'accepted', 'expired', name='status_types'),
                  nullable=False, default='awaiting'),
        sa.Column('created_at', sa.DateTime, nullable=False, default=sa.func),
    )

def downgrade():
    op.drop_table('matched_parking_space_list')

