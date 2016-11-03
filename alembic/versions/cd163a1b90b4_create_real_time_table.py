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
        sa.Column('waiting_user_id', sa.String(64),  nullable=False),
        sa.Column('waiting_user_latitude', sa.String(64), nullable=False),
        sa.Column('waiting_user_longitude', sa.Float, nullable=False),
        sa.Column('request_user_id', sa.Float, nullable=False),
        sa.Column('request_user_latitude', sa.Float, nullable=False),
        sa.Column('request_user_longitude', sa.Float, nullable=False),
        sa.Column('created_at', sa.DateTime, default=sa.func)
    )


def downgrade():
    op.drop_table('real_time')
