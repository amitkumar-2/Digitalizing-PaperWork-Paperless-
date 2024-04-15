"""little changes

Revision ID: 8ea4f9dc0ed6
Revises: c8ef8b504ddb
Create Date: 2024-04-15 11:20:58.852772

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8ea4f9dc0ed6'
down_revision = 'c8ef8b504ddb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('work_assigned_to_operator', schema=None) as batch_op:
        batch_op.add_column(sa.Column('check_fpa_status_at', sa.Integer(), nullable=True))
        batch_op.drop_column('completed_at_mid_shift')

    with op.batch_alter_table('work_assigned_to_operator_logs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('check_fpa_status_at', sa.Integer(), nullable=True))
        batch_op.drop_column('completed_at_mid_shift')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('work_assigned_to_operator_logs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('completed_at_mid_shift', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_column('check_fpa_status_at')

    with op.batch_alter_table('work_assigned_to_operator', schema=None) as batch_op:
        batch_op.add_column(sa.Column('completed_at_mid_shift', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_column('check_fpa_status_at')

    # ### end Alembic commands ###
