"""empty message

Revision ID: 24303a920dd8
Revises: a9123736678c
Create Date: 2018-02-24 07:25:43.258821

"""

# revision identifiers, used by Alembic.
revision = '24303a920dd8'
down_revision = 'a9123736678c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Blogs', sa.Column('title', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Blogs', 'title')
    # ### end Alembic commands ###
