"""empty message

Revision ID: 64342f63f638
Revises: c8f64381bfe1
Create Date: 2018-01-07 19:32:02.528834

"""

# revision identifiers, used by Alembic.
revision = '64342f63f638'
down_revision = 'c8f64381bfe1'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('chat_message', sa.Column('recipient_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_chat_message_read'), 'chat_message', ['read'], unique=False)
    op.create_index(op.f('ix_chat_message_recipient_id'), 'chat_message', ['recipient_id'], unique=False)
    op.create_foreign_key(None, 'chat_message', 'char', ['recipient_id'], ['id'])


def downgrade():
    op.drop_constraint(None, 'chat_message', type_='foreignkey')
    op.drop_index(op.f('ix_chat_message_recipient_id'), table_name='chat_message')
    op.drop_index(op.f('ix_chat_message_read'), table_name='chat_message')
    op.drop_column('chat_message', 'recipient_id')
