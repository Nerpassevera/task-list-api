"""Adds updates Goal model

Revision ID: 3edabf27ff58
Revises: 52c8b0992e23
Create Date: 2024-11-07 13:16:55.721590

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3edabf27ff58'
down_revision = '52c8b0992e23'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('goal', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.String(length=50), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('goal', schema=None) as batch_op:
        batch_op.drop_column('title')

    # ### end Alembic commands ###