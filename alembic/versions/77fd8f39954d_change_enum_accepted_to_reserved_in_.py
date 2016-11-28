"""change enum accepted to reserved in matched_parking_space table

Revision ID: 77fd8f39954d
Revises: 8053b268e06e
Create Date: 2016-11-21 08:23:12.199242

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77fd8f39954d'
down_revision = '8053b268e06e'
branch_labels = None
depends_on = None

def upgrade():

    op.add_column(
        'matched_parking_space_list',
        sa.Column(
            'statusB',
            sa.Enum('awaiting', 'rejected', 'reserved', 'expired', name='status_types'),
            nullable=True, default='awaiting'),
     )
    op.execute("""
        UPDATE matched_parking_space_list
        SET statusB = (
        select status from (select * from matched_parking_space_list) as B
        where matched_parking_space_list.plate = B.plate
        limit 1
        )
    """)
    op.drop_column('matched_parking_space_list', 'status')
    op.alter_column(
        'matched_parking_space_list',
        column_name='statusB',
        new_column_name='status',
        existing_type=sa.Enum('awaiting', 'rejected', 'reserved', 'expired', name='status_types'),
    )
    op.alter_column(
        'matched_parking_space_list',
        column_name='status',
        nullable=False,
        existing_type=sa.Enum('awaiting', 'rejected', 'reserved', 'expired', name='status_types'),
    )


def downgrade():
    op.add_column(
        'matched_parking_space_list',
        sa.Column(
            'statusB',
            sa.Enum('awaiting', 'rejected', 'accepted', 'expired', name='status_types'),
            nullable=True, default='awaiting'),
    )
    op.execute("""
        UPDATE matched_parking_space_list
        SET statusB = (
        select status from (select * from matched_parking_space_list) as B
        where matched_parking_space_list.plate = B.plate
        limit 1
        )
    """)
    op.drop_column('matched_parking_space_list', 'status')
    op.alter_column(
        'matched_parking_space_list',
        column_name='statusB',
        new_column_name='status',
        existing_type=sa.Enum('awaiting', 'rejected', 'accepted', 'expired', name='status_types'),
    )
    op.alter_column(
        'matched_parking_space_list',
        column_name='status',
        nullable=False,
        existing_type=sa.Enum('awaiting', 'rejected', 'accepted', 'expired', name='status_types'),
    )

