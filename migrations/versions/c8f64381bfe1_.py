"""empty message

Revision ID: c8f64381bfe1
Revises: cd4833ee5f8a
Create Date: 2018-01-07 13:27:23.674117

"""

# revision identifiers, used by Alembic.
revision = 'c8f64381bfe1'
down_revision = 'cd4833ee5f8a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('chat_message', sa.Column('message', sa.Text(), nullable=True))
    op.create_unique_constraint(None, 'chat_room', ['id'])


def downgrade():
    op.drop_constraint(None, 'chat_room', type_='unique')
    op.drop_column('chat_message', 'message')
