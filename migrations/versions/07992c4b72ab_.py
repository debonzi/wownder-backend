"""empty message

Revision ID: 07992c4b72ab
Revises: None
Create Date: 2017-12-17 19:09:17.874115

"""

# revision identifiers, used by Alembic.
revision = '07992c4b72ab'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('battletag', sa.String(length=80), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('oauth_token', sa.String(length=50), nullable=True),
    sa.Column('language', sa.String(length=5), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('battletag'),
    sa.UniqueConstraint('email')
    )

    op.create_table('char',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=33), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.Column('realm', sa.String(length=30), nullable=True),
    sa.Column('char_class', sa.SmallInteger(), nullable=True),
    sa.Column('race', sa.SmallInteger(), nullable=True),
    sa.Column('gender', sa.SmallInteger(), nullable=True),
    sa.Column('level', sa.SmallInteger(), nullable=True),
    sa.Column('thumbnail', sa.String(length=255), nullable=True),
    sa.Column('last_bn_update', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('char_ix', 'char', ['name', 'realm'], unique=True)
    op.create_index(op.f('ix_char_user_id'), 'char', ['user_id'], unique=False)
    op.create_index(op.f('ix_char_uuid'), 'char', ['uuid'], unique=True)

    op.create_table('pvp_char_stats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('char_id', sa.Integer(), nullable=True),
    sa.Column('b2_current_rating', sa.Integer(), nullable=False),
    sa.Column('b3_current_rating', sa.Integer(), nullable=False),
    sa.Column('b2_best_rating', sa.Integer(), nullable=False),
    sa.Column('b3_best_rating', sa.Integer(), nullable=False),
    sa.Column('rbg_current_rating', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['char_id'], ['char.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_pvp_char_stats_b2_current_rating'), 'pvp_char_stats', ['b2_current_rating'], unique=False)
    op.create_index(op.f('ix_pvp_char_stats_b3_current_rating'), 'pvp_char_stats', ['b3_current_rating'], unique=False)
    op.create_index(op.f('ix_pvp_char_stats_char_id'), 'pvp_char_stats', ['char_id'], unique=False)
    op.create_index(op.f('ix_pvp_char_stats_rbg_current_rating'), 'pvp_char_stats', ['rbg_current_rating'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_pvp_char_stats_rbg_current_rating'), table_name='pvp_char_stats')
    op.drop_index(op.f('ix_pvp_char_stats_char_id'), table_name='pvp_char_stats')
    op.drop_index(op.f('ix_pvp_char_stats_b3_current_rating'), table_name='pvp_char_stats')
    op.drop_index(op.f('ix_pvp_char_stats_b2_current_rating'), table_name='pvp_char_stats')
    op.drop_table('pvp_char_stats')
    op.drop_index(op.f('ix_char_uuid'), table_name='char')
    op.drop_index(op.f('ix_char_user_id'), table_name='char')
    op.drop_index('char_ix', table_name='char')
    op.drop_table('char')
    op.drop_table('user')
