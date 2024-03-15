"""Created some database tables

Revision ID: c20c690dd4af
Revises: f301e5b33b0e
Create Date: 2024-03-15 11:51:08.355582

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c20c690dd4af'
down_revision = 'f301e5b33b0e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('parameters_info', schema=None) as batch_op:
        batch_op.add_column(sa.Column('readings_status', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('parameters_info', schema=None) as batch_op:
        batch_op.drop_column('readings_status')

    # ### end Alembic commands ###