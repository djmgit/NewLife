"""empty message

Revision ID: 7b1d66baf65c
Revises: 24303a920dd8
Create Date: 2018-02-25 23:11:18.895168

"""

# revision identifiers, used by Alembic.
revision = '7b1d66baf65c'
down_revision = '24303a920dd8'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Blogs', sa.Column('author_email', sa.String(), nullable=True))
    op.add_column('Blogs', sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.drop_column('Blogs', 'timestamp')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Blogs', sa.Column('timestamp', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('Blogs', 'time_created')
    op.drop_column('Blogs', 'author_email')
    # ### end Alembic commands ###
