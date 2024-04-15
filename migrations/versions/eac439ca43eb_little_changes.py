"""little changes

Revision ID: eac439ca43eb
Revises: 1d586887c58f
Create Date: 2024-04-12 17:51:37.536079

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'eac439ca43eb'
down_revision = '1d586887c58f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('check_sheet_data', schema=None) as batch_op:
        batch_op.alter_column('station_id',
               existing_type=mysql.VARCHAR(length=15),
               nullable=False)
        batch_op.drop_index('station_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('check_sheet_data', schema=None) as batch_op:
        batch_op.create_index('station_id', ['station_id'], unique=True)
        batch_op.alter_column('station_id',
               existing_type=mysql.VARCHAR(length=15),
               nullable=True)

    # ### end Alembic commands ###
