"""little changes

Revision ID: ed24503871ab
Revises: c4ae2c645ca3
Create Date: 2024-04-29 12:09:50.950078

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ed24503871ab'
down_revision = 'c4ae2c645ca3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notify_to_incharge', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_date', sa.Date(), nullable=True))
        batch_op.add_column(sa.Column('created_time', sa.Time(), nullable=True))
        batch_op.drop_column('created_at')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notify_to_incharge', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', mysql.DATETIME(), nullable=True))
        batch_op.drop_column('created_time')
        batch_op.drop_column('created_date')

    # ### end Alembic commands ###