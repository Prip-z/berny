"""add_pg_trgm_extension

Revision ID: 01e40d9ebb89
Revises: 313383a1d71e
Create Date: 2026-08-07 13:20:00.280002

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "01e40d9ebb89"
down_revision: str | Sequence[str] | None = "313383a1d71e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")


def downgrade() -> None:
    """Downgrade schema."""
