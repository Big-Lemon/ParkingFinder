"""create_check_out_parking_space_table

Revision ID: 7c7dc436640a
Revises: 1242db7e3d9c
Create Date: 2016-11-03 13:28:49.181013

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c7dc436640a'
down_revision = '1242db7e3d9c'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'check_out_parking_space',
        sa.Column('user_id', sa.String(64), sa.ForeignKey('users.user_id'), primary_key=True),
        sa.Column('latitude', sa.Float, nullable=False),
        sa.Column('longitude', sa.Float, nullable=False),
        sa.Column('created_at', sa.DateTime, default=sa.func),
        sa.Column('level', sa.Integer, nullable=True),
        sa.Column('description', sa.String(500), nullable=True)
    )


def downgrade():
    op.drop_table('check_out_parking_space')
