"""empty message

Revision ID: d641536fddc6
Revises: 07992c4b72ab
Create Date: 2017-12-19 00:15:11.667774

"""

# revision identifiers, used by Alembic.
revision = 'd641536fddc6'
down_revision = '07992c4b72ab'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('profile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('char_id', sa.Integer(), nullable=False),
    sa.Column('role', sa.String(length=20), nullable=False),
    sa.Column('faction', sa.String(length=10), nullable=False),
    sa.Column('listed_2s', sa.Boolean(), nullable=False),
    sa.Column('listed_3s', sa.Boolean(), nullable=False),
    sa.Column('voice', sa.Boolean(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['char_id'], ['char.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_profile_char_id'), 'profile', ['char_id'], unique=False)
    op.create_index(op.f('ix_profile_faction'), 'profile', ['faction'], unique=False)
    op.create_index(op.f('ix_profile_listed_2s'), 'profile', ['listed_2s'], unique=False)
    op.create_index(op.f('ix_profile_listed_3s'), 'profile', ['listed_3s'], unique=False)
    op.create_index(op.f('ix_profile_role'), 'profile', ['role'], unique=False)
    op.create_index(op.f('ix_profile_voice'), 'profile', ['voice'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_profile_voice'), table_name='profile')
    op.drop_index(op.f('ix_profile_role'), table_name='profile')
    op.drop_index(op.f('ix_profile_listed_3s'), table_name='profile')
    op.drop_index(op.f('ix_profile_listed_2s'), table_name='profile')
    op.drop_index(op.f('ix_profile_faction'), table_name='profile')
    op.drop_index(op.f('ix_profile_char_id'), table_name='profile')
    op.drop_table('profile')
