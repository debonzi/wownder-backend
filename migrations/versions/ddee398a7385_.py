"""empty message

Revision ID: ddee398a7385
Revises: 59365c3bea16
Create Date: 2018-01-28 20:45:24.642416

"""

# revision identifiers, used by Alembic.
revision = 'ddee398a7385'
down_revision = '59365c3bea16'

from alembic import op


def upgrade():
    op.create_index('char_name_realm_region_un', 'char', ['name', 'realm', 'region'], unique=True)
    op.drop_index('char_ix', table_name='char')


def downgrade():
    op.create_index('char_ix', 'char', ['name', 'realm'], unique=True)
    op.drop_index('char_name_realm_region_un', table_name='char')
