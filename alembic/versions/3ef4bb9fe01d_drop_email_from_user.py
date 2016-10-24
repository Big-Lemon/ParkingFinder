"""drop email from user

Revision ID: 3ef4bb9fe01d
Revises: afde421ba47b
Create Date: 2016-10-22 19:54:10.345846

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ef4bb9fe01d'
down_revision = 'afde421ba47b'
branch_labels = None
depends_on = None

def upgrade():
    op.drop_column('users', 'email')


def downgrade():
    op.add_column(
        'users',
        sa.Column('email', sa.String(255), nullable=True)
    )

