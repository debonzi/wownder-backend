"""empty message

Revision ID: cd4833ee5f8a
Revises: d641536fddc6
Create Date: 2018-01-06 17:55:02.687933

"""

# revision identifiers, used by Alembic.
revision = 'cd4833ee5f8a'
down_revision = 'd641536fddc6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('chat_room',
    sa.Column('id', sa.String(length=33), nullable=False),
    sa.Column('char_1_id', sa.Integer(), nullable=False),
    sa.Column('char_2_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['char_1_id'], ['char.id'], ),
    sa.ForeignKeyConstraint(['char_2_id'], ['char.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index('chars_un', 'chat_room', ['char_1_id', 'char_2_id'], unique=True)
    op.create_index(op.f('ix_chat_room_char_1_id'), 'chat_room', ['char_1_id'], unique=False)
    op.create_index(op.f('ix_chat_room_char_2_id'), 'chat_room', ['char_2_id'], unique=False)
    op.create_table('chat_message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('room_id', sa.String(length=33), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('read', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['room_id'], ['chat_room.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['char.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chat_message_room_id'), 'chat_message', ['room_id'], unique=False)
    op.create_index(op.f('ix_chat_message_sender_id'), 'chat_message', ['sender_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_chat_message_sender_id'), table_name='chat_message')
    op.drop_index(op.f('ix_chat_message_room_id'), table_name='chat_message')
    op.drop_table('chat_message')
    op.drop_index(op.f('ix_chat_room_char_2_id'), table_name='chat_room')
    op.drop_index(op.f('ix_chat_room_char_1_id'), table_name='chat_room')
    op.drop_index('chars_un', table_name='chat_room')
    op.drop_table('chat_room')
