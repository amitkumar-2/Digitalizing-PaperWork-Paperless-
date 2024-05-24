"""little changes

Revision ID: 5d536efd6f7b
Revises: 4ab8cc05c75f
Create Date: 2024-05-23 17:31:07.384422

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d536efd6f7b'
down_revision = '4ab8cc05c75f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('work_assigned_to_operator', schema=None) as batch_op:
        batch_op.drop_index('ix_work_assigned_to_operator_task_id')
        batch_op.create_index(batch_op.f('ix_work_assigned_to_operator_task_id'), ['task_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('work_assigned_to_operator', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_work_assigned_to_operator_task_id'))
        batch_op.create_index('ix_work_assigned_to_operator_task_id', ['task_id'], unique=True)

    # ### end Alembic commands ###
