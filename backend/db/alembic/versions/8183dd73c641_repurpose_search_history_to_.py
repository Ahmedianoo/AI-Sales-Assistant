"""Repurpose search_history to conversations table structure

Revision ID: 8183dd73c641
Revises: baca3fa31e6b
Create Date: 2025-10-02 09:04:13.044805

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import text 

# revision identifiers, used by Alembic.
revision: str = '8183dd73c641'
down_revision: Union[str, Sequence[str], None] = 'baca3fa31e6b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.rename_table('search_history', 'conversations')
    op.execute(text("TRUNCATE TABLE conversations RESTART IDENTITY CASCADE;"))
    op.drop_column('conversations', 'search_id')

    # --- 4. CREATE NEW UUID PK COLUMN ---
    # Create the new thread_id column with UUID type and server-side default.
    op.add_column('conversations', 
                  sa.Column('thread_id', sa.Uuid(), 
                            primary_key=True, 
                            server_default=sa.text('gen_random_uuid()'), 
                            nullable=False)
    )

    op.alter_column('conversations', 'query', new_column_name='title')
    op.alter_column('conversations', 'searched_at', new_column_name='created_at')


def downgrade() -> None:
    """Downgrade schema: Restore table 'conversations' to original 'search_history' structure."""
    
    # We must operate on the current table name: 'conversations'
    op.alter_column('conversations', 'created_at', new_column_name='searched_at')
    op.alter_column('conversations', 'title', new_column_name='query')
    
    op.drop_column('conversations', 'thread_id')
    
    # Recreate the old integer PK column.
    op.add_column('conversations', 
                  sa.Column('search_id', sa.Integer(), 
                            primary_key=True, 
                            nullable=False, 
                            autoincrement=True)
    )

    # --- 3. RENAME TABLE OPERATION ---
    # This safely renames the table back to the original name
    op.rename_table('conversations', 'search_history')