"""sample_vehicle

Revision ID: 27065f41bf8a
Revises: 68bf50468c01
Create Date: 2016-10-31 15:11:59.285161

"""
from alembic import op
import sqlalchemy as sa

from datetime import datetime
from sqlalchemy.sql import table, column

# revision identifiers, used by Alembic.
revision = '27065f41bf8a'
down_revision = '68bf50468c01'
branch_labels = None
depends_on = None


vehicles_table = table(
    'vehicles',
    column('plate', sa.String),
    column('brand', sa.String),
    column('model', sa.String),
    column('color', sa.String),
    column('year', sa.Integer),
)


data = [
    {
        'plate': '6ELA725',
        'brand': 'Toyota',
        'model': 'Matrix',
        'color': 'Golden',
        'year': 2009,
    },
    {
        'plate': '6ELA540',
        'brand': 'Toyota',
        'model': 'Prius',
        'color': 'Sliver',
        'year': 2009,
    },
    {
        'plate': '6TRJ224',
        'brand': 'Nissan',
        'model': 'Altima',
        'color': 'White',
        'year': 2010,
    },
    {
        'plate': 'ANRCHST',
        'brand': 'Porsche',
        'model': 'Boxster',
        'color': 'Black',
        'year': 2008,
    },
    {
        'plate': '4JTY881',
        'brand': 'Ford',
        'model': 'Expedition',
        'color': 'yellow',
        'year': 2000,
    },
]


def upgrade():
    op.bulk_insert(
        vehicles_table,
        data
    )


def downgrade():
    for row in data:
        op.execute(
            vehicles_table.delete().where(
                vehicles_table.c.plate == row['plate']
            )
        )
