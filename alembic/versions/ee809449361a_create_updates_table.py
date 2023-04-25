"""create updates table

Revision ID: ee809449361a
Revises: 
Create Date: 2023-04-24 07:45:36.114802

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee809449361a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('updates', 
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('updates')
    pass
