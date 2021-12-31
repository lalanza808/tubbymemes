"""add meme sync flag

Revision ID: f6f695a38339
Revises: f15cd9fa0f06
Create Date: 2021-12-31 11:05:28.153450

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6f695a38339'
down_revision = 'f15cd9fa0f06'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('memes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('synced', sa.Boolean(), nullable=True))



def downgrade():
    with op.batch_alter_table('memes', schema=None) as batch_op:
        batch_op.drop_column('synced')
