"""little changes

Revision ID: ed13779cca0f
Revises: f7578f2cd2e3
Create Date: 2024-05-03 12:53:16.623241

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed13779cca0f'
down_revision = 'f7578f2cd2e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reading_params_logs', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_reading_params_logs_date'), ['date'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reading_params_logs', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_reading_params_logs_date'))

    # ### end Alembic commands ###
