"""add comment column to updates table

Revision ID: d7f24bb1daa4
Revises: ee809449361a
Create Date: 2023-04-24 07:59:21.159450

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7f24bb1daa4'
down_revision = 'ee809449361a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("updates", 
                  sa.Column('comment', sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column("updates",'comment')
    pass
