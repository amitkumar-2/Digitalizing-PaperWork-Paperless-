"""little changes

Revision ID: 18b81a8eae68
Revises: 1810533c3686
Create Date: 2024-03-19 16:47:13.633069

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '18b81a8eae68'
down_revision = '1810533c3686'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('check_sheet',
    sa.Column('csp_id', sa.String(length=15), nullable=False),
    sa.Column('csp_name', sa.String(length=300), nullable=False),
    sa.Column('added_by_owner', sa.String(length=30), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('csp_id')
    )
    with op.batch_alter_table('check_sheet_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))
        batch_op.add_column(sa.Column('oprtr_employee_id', sa.String(length=20), nullable=False))
        batch_op.add_column(sa.Column('flrInchr_employee_id', sa.String(length=30), nullable=True))
        batch_op.add_column(sa.Column('status_datas', sa.String(length=1500), nullable=False))
        batch_op.add_column(sa.Column('time', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('date', sa.DateTime(), nullable=True))
        batch_op.drop_column('added_by_owner')
        batch_op.drop_column('csp_name')
        batch_op.drop_column('date_time')

    with op.batch_alter_table('check_sheet_data_logs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('time', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('date', sa.DateTime(), nullable=True))
        batch_op.drop_column('date_time')

    with op.batch_alter_table('parameters_info', schema=None) as batch_op:
        batch_op.add_column(sa.Column('time', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('date', sa.DateTime(), nullable=True))
        batch_op.drop_column('date_time')

    with op.batch_alter_table('params_ucl_lcl', schema=None) as batch_op:
        batch_op.add_column(sa.Column('time', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('date', sa.DateTime(), nullable=True))
        batch_op.drop_column('date_time')

    with op.batch_alter_table('parts_info', schema=None) as batch_op:
        batch_op.add_column(sa.Column('time', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('date', sa.DateTime(), nullable=True))
        batch_op.drop_column('date_time')

    with op.batch_alter_table('processes_info', schema=None) as batch_op:
        batch_op.add_column(sa.Column('time', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('date', sa.DateTime(), nullable=True))
        batch_op.drop_column('date_time')

    with op.batch_alter_table('stations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('added_time', sa.DateTime(), nullable=True))

    with op.batch_alter_table('work_assigned_to_operator', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', sa.DateTime(), nullable=True))
        batch_op.drop_column('date_time')

    with op.batch_alter_table('work_assigned_to_operator_logs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', sa.DateTime(), nullable=True))
        batch_op.drop_column('date_time')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('work_assigned_to_operator_logs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_time', mysql.DATETIME(), nullable=True))
        batch_op.drop_column('date')

    with op.batch_alter_table('work_assigned_to_operator', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_time', mysql.DATETIME(), nullable=True))
        batch_op.drop_column('date')

    with op.batch_alter_table('stations', schema=None) as batch_op:
        batch_op.drop_column('added_time')

    with op.batch_alter_table('processes_info', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_time', mysql.DATETIME(), nullable=True))
        batch_op.drop_column('date')
        batch_op.drop_column('time')

    with op.batch_alter_table('parts_info', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_time', mysql.DATETIME(), nullable=True))
        batch_op.drop_column('date')
        batch_op.drop_column('time')

    with op.batch_alter_table('params_ucl_lcl', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_time', mysql.DATETIME(), nullable=True))
        batch_op.drop_column('date')
        batch_op.drop_column('time')

    with op.batch_alter_table('parameters_info', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_time', mysql.DATETIME(), nullable=True))
        batch_op.drop_column('date')
        batch_op.drop_column('time')

    with op.batch_alter_table('check_sheet_data_logs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_time', mysql.DATETIME(), nullable=True))
        batch_op.drop_column('date')
        batch_op.drop_column('time')

    with op.batch_alter_table('check_sheet_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_time', mysql.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column('csp_name', mysql.VARCHAR(length=300), nullable=False))
        batch_op.add_column(sa.Column('added_by_owner', mysql.VARCHAR(length=30), nullable=False))
        batch_op.drop_column('date')
        batch_op.drop_column('time')
        batch_op.drop_column('status_datas')
        batch_op.drop_column('flrInchr_employee_id')
        batch_op.drop_column('oprtr_employee_id')
        batch_op.drop_column('id')

    op.drop_table('check_sheet')
    # ### end Alembic commands ###
