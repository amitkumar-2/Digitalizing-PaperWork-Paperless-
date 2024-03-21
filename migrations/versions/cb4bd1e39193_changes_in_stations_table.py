"""changes in stations table

Revision ID: cb4bd1e39193
Revises: c20c690dd4af
Create Date: 2024-03-16 14:45:59.021364

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'cb4bd1e39193'
down_revision = 'c20c690dd4af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('parameters_info', schema=None) as batch_op:
        batch_op.add_column(sa.Column('readings_is_available', sa.Boolean(), nullable=True))
        batch_op.drop_column('readings_status')

    with op.batch_alter_table('stations', schema=None) as batch_op:
        batch_op.alter_column('station_id',
               existing_type=mysql.VARCHAR(length=15),
               type_=sa.String(length=25),
               existing_nullable=False)
        batch_op.alter_column('line_no',
               existing_type=mysql.VARCHAR(length=10),
               type_=sa.String(length=20),
               existing_nullable=False)
        batch_op.alter_column('floor_no',
               existing_type=mysql.VARCHAR(length=10),
               type_=sa.String(length=20),
               existing_nullable=False)
        batch_op.drop_column('id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.alter_column('floor_no',
               existing_type=sa.String(length=20),
               type_=mysql.VARCHAR(length=10),
               existing_nullable=False)
        batch_op.alter_column('line_no',
               existing_type=sa.String(length=20),
               type_=mysql.VARCHAR(length=10),
               existing_nullable=False)
        batch_op.alter_column('station_id',
               existing_type=sa.String(length=25),
               type_=mysql.VARCHAR(length=15),
               existing_nullable=False)

    with op.batch_alter_table('parameters_info', schema=None) as batch_op:
        batch_op.add_column(sa.Column('readings_status', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
        batch_op.drop_column('readings_is_available')

    # ### end Alembic commands ###