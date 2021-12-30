"""meme approval

Revision ID: f15cd9fa0f06
Revises: c548cc54ee17
Create Date: 2021-12-30 13:11:10.706513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f15cd9fa0f06'
down_revision = 'c548cc54ee17'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('memes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('approved', sa.Boolean(), nullable=True))



def downgrade():
    with op.batch_alter_table('memes', schema=None) as batch_op:
        batch_op.drop_column('approved')
