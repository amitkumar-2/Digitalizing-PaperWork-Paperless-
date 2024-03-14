"""added some tables in database

Revision ID: 0acc7a0f37e8
Revises: 258484a86d13
Create Date: 2024-03-12 15:35:07.611266

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0acc7a0f37e8'
down_revision = '258484a86d13'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('station_info',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=True),
    sa.Column('station_id', sa.String(length=15), nullable=False),
    sa.Column('total_assigned_task', sa.Integer(), nullable=False),
    sa.Column('left_for_rework', sa.Integer(), nullable=True),
    sa.Column('passed', sa.Integer(), nullable=True),
    sa.Column('filled', sa.Integer(), nullable=True),
    sa.Column('failed', sa.Integer(), nullable=True),
    sa.Column('start_shift_timing', sa.Time(), nullable=False),
    sa.Column('end_shift_timing', sa.Time(), nullable=False),
    sa.Column('date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('station_id')
    )
    op.create_table('station_info_logs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('station_id', sa.String(length=15), nullable=False),
    sa.Column('total_assigned_task', sa.Integer(), nullable=False),
    sa.Column('left_for_rework', sa.Integer(), nullable=True),
    sa.Column('passed', sa.Integer(), nullable=True),
    sa.Column('filled', sa.Integer(), nullable=True),
    sa.Column('failed', sa.Integer(), nullable=True),
    sa.Column('start_shift_timing', sa.Time(), nullable=False),
    sa.Column('end_shift_timing', sa.Time(), nullable=False),
    sa.Column('date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('station_info_logs')
    op.drop_table('station_info')
    # ### end Alembic commands ###
