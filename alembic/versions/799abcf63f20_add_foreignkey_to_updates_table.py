"""add foreignkey to updates table

Revision ID: 799abcf63f20
Revises: 8235f7f15e98
Create Date: 2023-04-24 08:21:24.489601

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '799abcf63f20'
down_revision = '8235f7f15e98'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("updates", sa.Column(
        'owner_id', sa.Integer(), nullable=False)),
    op.create_foreign_key('updates_users_fk', source_table='updates', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('updates_users_fk', table_name='updates')
    op.drop_column('updates', 'owner_id')
    pass
