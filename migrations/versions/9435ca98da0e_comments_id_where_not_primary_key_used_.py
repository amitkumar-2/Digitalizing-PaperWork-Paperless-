"""Comments ID where not primary key used as ID

Revision ID: 9435ca98da0e
Revises: 7ab17214a5e4
Create Date: 2024-03-13 12:09:41.803073

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9435ca98da0e'
down_revision = '7ab17214a5e4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('parameters_info', schema=None) as batch_op:
        batch_op.drop_column('id')

    with op.batch_alter_table('parts_info', schema=None) as batch_op:
        batch_op.drop_column('id')

    with op.batch_alter_table('processes_info', schema=None) as batch_op:
        batch_op.drop_column('id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('processes_info', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', mysql.INTEGER(), autoincrement=False, nullable=True))

    with op.batch_alter_table('parts_info', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', mysql.INTEGER(), autoincrement=False, nullable=True))

    with op.batch_alter_table('parameters_info', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', mysql.INTEGER(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###