"""init suchwowx

Revision ID: 40734564d415
Revises:
Create Date: 2021-12-28 22:05:09.994215

"""
from uuid import uuid4

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '40734564d415'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    mods_table = op.create_table('moderators',
        sa.Column('id', sa.Integer, autoincrement=True, nullable=False, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='moderators_user_id_fkey'),
    )
    users_table = op.create_table('users',
        sa.Column('id', sa.Integer, autoincrement=True, nullable=False),
        sa.Column('register_date', sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column('last_login_date', sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column('verified', sa.Boolean, autoincrement=False, nullable=True),
        sa.Column('public_address', sa.String(180), autoincrement=False, nullable=True),
        sa.Column('nonce', sa.String(180), autoincrement=False, nullable=True),
        sa.Column('nonce_date', sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column('handle', sa.String(40), autoincrement=False, nullable=True, ),
        sa.Column('bio', sa.String(600), autoincrement=False, nullable=True),
        sa.Column('profile_image', sa.String(300), autoincrement=False, nullable=True),
        sa.Column('website_url', sa.String(120), autoincrement=False, nullable=True),
        sa.Column('moderator_id', sa.Integer, nullable=True),
        sa.PrimaryKeyConstraint('id', name='users_pkey'),
        sa.UniqueConstraint('handle', name='users_handle_key'),
        sa.ForeignKeyConstraint(['moderator_id'], ['moderators.id'], name='users_user_id_fkey'),
    )
    memes_table = op.create_table('memes',
        sa.Column('id', sa.String(80), server_default=uuid4().hex, autoincrement=False, nullable=False),
        sa.Column('user_id', sa.Integer, autoincrement=False, nullable=True),
        sa.Column('create_date', sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column('title', sa.String(80), autoincrement=False, nullable=True),
        sa.Column('description', sa.String(300), autoincrement=False, nullable=True),
        sa.Column('file_name', sa.String(300), autoincrement=False, nullable=True),
        sa.Column('minted', sa.Boolean, autoincrement=False, nullable=True),
        sa.Column('meta_ipfs_hash', sa.String(100), autoincrement=False, nullable=True),
        sa.Column('meme_ipfs_hash', sa.String(100), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='artwork_user_id_fkey'),
        sa.PrimaryKeyConstraint('id', name='artwork_pkey'),
        sa.UniqueConstraint('meta_ipfs_hash', name='memes_meta_ipfs_hash_key'),
        sa.UniqueConstraint('meme_ipfs_hash', name='memes_meme_ipfs_hash_key')
    )

def downgrade():
    op.drop_table('moderators')
    op.drop_table('users')
    op.drop_table('memes')
