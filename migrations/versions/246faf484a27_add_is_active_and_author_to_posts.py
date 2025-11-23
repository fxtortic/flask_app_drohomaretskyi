"""Add is_active and author to posts

Revision ID: 246faf484a27
Revises:
Create Date: 2025-11-23 21:44:44.187430

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "246faf484a27"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("posts", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "is_active",
                sa.Boolean(),
                nullable=False,
                server_default=sa.true(),
            )
        )
        batch_op.add_column(
            sa.Column(
                "author",
                sa.String(length=20),
                nullable=False,
                server_default="Anonymous",
            )
        )


def downgrade():
    with op.batch_alter_table("posts", schema=None) as batch_op:
        batch_op.drop_column("author")
        batch_op.drop_column("is_active")
