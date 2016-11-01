"""create_registered_vehicles_table

Revision ID: 68bf50468c01
Revises: 8fbaade4734b
Create Date: 2016-10-29 23:55:27.500038

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68bf50468c01'
down_revision = '8fbaade4734b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'registered_vehicles',
        sa.Column('user_id', sa.String(64), sa.ForeignKey('users.user_id')),
        sa.Column('plate', sa.String(7), sa.ForeignKey('vehicles.plate')),
        sa.PrimaryKeyConstraint('user_id', 'plate',),
    )


def downgrade():
    op.drop_table('registered_vehicles')
