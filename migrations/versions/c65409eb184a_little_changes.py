"""little changes

Revision ID: c65409eb184a
Revises: ab842661ceae
Create Date: 2024-05-01 12:05:55.460859

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c65409eb184a'
down_revision = 'ab842661ceae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('failed_items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('part_no', sa.String(length=20), nullable=True))

    with op.batch_alter_table('notify_to_incharge', schema=None) as batch_op:
        batch_op.add_column(sa.Column('notification_id', sa.Integer(), autoincrement=True, nullable=False))
        batch_op.drop_column('id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notify_to_incharge', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_column('notification_id')

    with op.batch_alter_table('failed_items', schema=None) as batch_op:
        batch_op.drop_column('part_no')

    # ### end Alembic commands ###