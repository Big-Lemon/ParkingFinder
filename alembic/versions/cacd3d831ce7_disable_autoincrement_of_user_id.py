"""disable autoincrement of user_id

Revision ID: cacd3d831ce7
Revises: 3ef4bb9fe01d
Create Date: 2016-10-22 19:55:41.918787

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cacd3d831ce7'
down_revision = '3ef4bb9fe01d'
branch_labels = None
depends_on = None

def upgrade():
    op.alter_column('users', 'user_id', type_=sa.String(64), autoincrement=False)


def downgrade():
    op.alter_column('users', 'user_id', type_=sa.String(64), autoincrement=True)

