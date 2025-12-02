"""add password_hash to users

Revision ID: 3fc1e0664bc0
Revises: 2a0e397fa2c2
Create Date: 2025-12-02 22:02:58.925365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3fc1e0664bc0'
down_revision = '2a0e397fa2c2'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("password_hash", sa.String(length=128), nullable=True)
        )


def downgrade():
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_column("password_hash")