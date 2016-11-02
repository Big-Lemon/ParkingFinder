"""create_real_time_table

Revision ID: cd163a1b90b4
Revises: 0e3813330b6b
Create Date: 2016-11-02 21:54:10.592331

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd163a1b90b4'
down_revision = '0e3813330b6b'
branch_labels = None
depends_on = None

def upgrade():
     op.create_table(
        'real_time',
        sa.Column('key', sa.String(32), primary_key=True),
        sa.Column('user_one_id', sa.String(64),  nullable=False),
        sa.Column('user_two_id', sa.String(64), nullable=False),
        sa.Column('latitude_one', sa.Float, nullable=False),
        sa.Column('longitude_one', sa.Float, nullable=False),
        sa.Column('latitude_two', sa.Float, nullable=False),
        sa.Column('longitude_two', sa.Float, nullable=False),
        sa.Column('created_at', sa.DateTime, default=sa.func)
    )


def downgrade():
    op.drop_table('real_time')
