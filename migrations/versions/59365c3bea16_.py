"""empty message

Revision ID: 59365c3bea16
Revises: 64342f63f638
Create Date: 2018-01-28 02:27:23.910253

"""

# revision identifiers, used by Alembic.
revision = '59365c3bea16'
down_revision = '64342f63f638'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('char', sa.Column('region', sa.String(length=2), nullable=True))
    op.execute("UPDATE char SET region='us'")
    op.alter_column('char', 'region', nullable=False)
    op.create_index(op.f('ix_char_region'), 'char', ['region'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_char_region'), table_name='char')
    op.drop_column('char', 'region')
