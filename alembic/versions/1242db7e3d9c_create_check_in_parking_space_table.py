"""create_check_in_parking_space_table

Revision ID: 1242db7e3d9c
Revises: fa89180e982f
Create Date: 2016-11-03 13:15:31.850199

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1242db7e3d9c'
down_revision = 'fa89180e982f'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'check_in_parking_space',
        sa.Column('user_id', sa.String(64), sa.ForeignKey('users.user_id'), primary_key=True),
        sa.Column('latitude', sa.Float, nullable=False),
        sa.Column('longitude', sa.Float, nullable=False),
        sa.Column('created_at', sa.DateTime, default=sa.func),
        sa.Column('level', sa.Integer, nullable=True),
        sa.Column('description', sa.String(500), nullable=True)
    )


def downgrade():
    op.drop_table('check_in_parking_space')
