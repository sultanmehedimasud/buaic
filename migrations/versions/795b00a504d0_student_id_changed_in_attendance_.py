"""Student ID changed in Attendance database

Revision ID: 795b00a504d0
Revises: 32307c120809
Create Date: 2024-04-14 23:46:34.698014

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '795b00a504d0'
down_revision = '32307c120809'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('attendance', schema=None) as batch_op:
        batch_op.add_column(sa.Column('student_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint('attendance_ibfk_2', type_='foreignkey')
        batch_op.create_foreign_key(None, 'user', ['student_id'], ['id'])
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('attendance', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('attendance_ibfk_2', 'user', ['user_id'], ['id'])
        batch_op.drop_column('student_id')

    # ### end Alembic commands ###
