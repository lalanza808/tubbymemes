"""init suchwowx

Revision ID: 53c117fcef3f
Revises:
Create Date: 2022-01-10 00:44:36.231037

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53c117fcef3f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('remotes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('last_sync_date', sa.DateTime(), nullable=True),
    sa.Column('paused', sa.Boolean(), nullable=True),
    sa.Column('endpoint', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('register_date', sa.DateTime(), nullable=True),
    sa.Column('last_login_date', sa.DateTime(), nullable=True),
    sa.Column('verified', sa.Boolean(), nullable=True),
    sa.Column('public_address', sa.String(length=180), nullable=True),
    sa.Column('nonce', sa.String(length=180), nullable=True),
    sa.Column('nonce_date', sa.DateTime(), nullable=True),
    sa.Column('handle', sa.String(length=40), nullable=True),
    sa.Column('bio', sa.String(length=600), nullable=True),
    sa.Column('profile_image', sa.String(length=300), nullable=True),
    sa.Column('ipfs_hash', sa.String(length=100), nullable=True),
    sa.Column('wownero_address', sa.String(length=120), nullable=True),
    sa.Column('website_url', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('handle')
    )
    op.create_table('memes',
    sa.Column('id', sa.String(length=80), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('file_name', sa.String(length=200), nullable=True),
    sa.Column('meta_ipfs_hash', sa.String(length=100), nullable=True),
    sa.Column('meme_ipfs_hash', sa.String(length=100), nullable=True),
    sa.Column('title', sa.String(length=50), nullable=True),
    sa.Column('description', sa.String(length=400), nullable=True),
    sa.Column('minted', sa.Boolean(), nullable=True),
    sa.Column('approved', sa.Boolean(), nullable=True),
    sa.Column('synced', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('file_name'),
    sa.UniqueConstraint('meme_ipfs_hash'),
    sa.UniqueConstraint('meta_ipfs_hash')
    )
    op.create_table('moderators',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('moderators')
    op.drop_table('memes')
    op.drop_table('users')
    op.drop_table('remotes')
