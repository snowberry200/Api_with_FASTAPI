"""add users  table

Revision ID: 8235f7f15e98
Revises: d7f24bb1daa4
Create Date: 2023-04-24 08:06:01.099404

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8235f7f15e98'
down_revision = 'd7f24bb1daa4'
branch_labels = None
depends_on = None


def upgrade() :
    op.create_table('users',
                    sa.Column('id',sa.Integer(),nullable= False),
                    sa.Column('email',sa.String(),nullable=False),
                    sa.Column('password',sa.String(),nullable = False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone = True),server_default=sa.text('now()'),nullable= False),
                    sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('email'))
    pass


def downgrade() :
    op.drop_table('users')
    pass
