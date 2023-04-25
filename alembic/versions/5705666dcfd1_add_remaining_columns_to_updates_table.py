"""add remaining columns to updates table

Revision ID: 5705666dcfd1
Revises: 799abcf63f20
Create Date: 2023-04-24 08:37:02.148789

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5705666dcfd1'
down_revision = '799abcf63f20'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('updates',sa.Column('published', sa.Boolean(), nullable=False,server_default= "True",))
    op.add_column('updates',sa.Column('created_at',sa.TIMESTAMP(timezone=True), nullable=False,
                                      server_default=sa.text('Now()'),))
    pass


def downgrade():
    op.drop_column(table_name='updates',column_name='published'),
    op.drop_column(table_name='updates',column_name='created_at')
    pass
