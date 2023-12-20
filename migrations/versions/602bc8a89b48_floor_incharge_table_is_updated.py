"""floor incharge table is updated

Revision ID: 602bc8a89b48
Revises: 4b69aea1baa5
Create Date: 2023-12-16 10:07:02.176156

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '602bc8a89b48'
down_revision = '4b69aea1baa5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('floor_incharge', schema=None) as batch_op:
        batch_op.add_column(sa.Column('building_no', sa.String(length=30), nullable=False))
        batch_op.alter_column('location',
               existing_type=sa.VARCHAR(length=30),
               nullable=False)
        batch_op.drop_constraint('floor_incharge_location_key', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('floor_incharge', schema=None) as batch_op:
        batch_op.create_unique_constraint('floor_incharge_location_key', ['location'])
        batch_op.alter_column('location',
               existing_type=sa.VARCHAR(length=30),
               nullable=True)
        batch_op.drop_column('building_no')

    # ### end Alembic commands ###