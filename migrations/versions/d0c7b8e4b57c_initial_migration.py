"""Initial migration.

Revision ID: d0c7b8e4b57c
Revises:
Create Date: 2022-11-08 17:00:02.151921

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0c7b8e4b57c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    print('dg')
    # ### commands auto generated by Alembic - please adjust! ###
    #op.create_table('candidates',
    #sa.Column('id', sa.Integer(), nullable=False),
    #sa.Column('source', sa.String(length=50), nullable=True),
    #sa.Column('question', sa.String(length=15000), nullable=True),
    #sa.Column('answer', sa.String(length=15000), nullable=True),
    #sa.PrimaryKeyConstraint('id')
    #)
    #op.create_table('results',
    #sa.Column('chosen_answer', sa.String(length=15000), nullable=True),
    #sa.Column('modified_answer', sa.String(length=15000), nullable=True),
    #sa.Column('comments', sa.String(length=15000), nullable=False),
    #sa.PrimaryKeyConstraint('comments')
    #)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    #op.drop_table('review')
    #op.drop_table('restaurant')
    print('dg')
    # ### end Alembic commands ###