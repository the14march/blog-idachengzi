"""posts version 2

Revision ID: 81e42ce306a6
Revises: 0c43e751db15
Create Date: 2017-10-19 00:20:54.004417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81e42ce306a6'
down_revision = '0c43e751db15'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('strip', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'strip')
    # ### end Alembic commands ###
