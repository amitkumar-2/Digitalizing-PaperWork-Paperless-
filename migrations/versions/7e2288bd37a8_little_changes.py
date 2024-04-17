"""little changes

Revision ID: 7e2288bd37a8
Revises: 50dfe3a4f2c1
Create Date: 2024-04-12 17:56:42.040685

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e2288bd37a8'
down_revision = '50dfe3a4f2c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('check_sheet_data', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['oprtr_employee_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('check_sheet_data', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###