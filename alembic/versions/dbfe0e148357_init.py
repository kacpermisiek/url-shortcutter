"""Init

Revision ID: dbfe0e148357
Revises:
Create Date: 2025-02-12 13:58:54.589559

"""

import uuid
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "dbfe0e148357"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "url",
        sa.Column(
            "id",
            sa.UUID(),
            primary_key=True,
            index=True,
            default=lambda: str(uuid.uuid4()),
        ),
        sa.Column("url", sa.String(), index=True),
        sa.Column("short_suffix", sa.String(), index=True),
        sa.Column("visits", sa.Integer(), default=0),
        sa.Column("created_by_ip", sa.String(), nullable=True),
        sa.Column("created_by_user_agent", sa.String(), nullable=True),
        sa.UniqueConstraint("url"),
    )


def downgrade() -> None:
    op.drop_table("url")
