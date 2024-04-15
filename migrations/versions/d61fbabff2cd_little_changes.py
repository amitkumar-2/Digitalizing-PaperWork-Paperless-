"""little changes

Revision ID: d61fbabff2cd
Revises: b8ab8aba8600
Create Date: 2024-04-12 17:54:45.038785

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd61fbabff2cd'
down_revision = 'b8ab8aba8600'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('check_sheet_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))
        batch_op.drop_column('station_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('check_sheet_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('station_id', mysql.VARCHAR(length=15), nullable=False))
        batch_op.drop_column('id')

    # ### end Alembic commands ###
