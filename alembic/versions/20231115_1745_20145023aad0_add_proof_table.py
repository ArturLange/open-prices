"""add proof table

Revision ID: 20145023aad0
Revises: 43571a31006d
Create Date: 2023-11-15 17:45:38.424368

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20145023aad0"
down_revision: Union[str, None] = "43571a31006d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "proofs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("file_path", sa.String(), nullable=False),
        sa.Column("mimetype", sa.String(), nullable=True),
        sa.Column("owner", sa.String(), nullable=True),
        sa.Column(
            "created",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_proofs_created"), "proofs", ["created"], unique=False)
    op.create_index(op.f("ix_proofs_id"), "proofs", ["id"], unique=False)
    op.create_index(op.f("ix_proofs_mimetype"), "proofs", ["mimetype"], unique=False)
    op.create_index(op.f("ix_proofs_owner"), "proofs", ["owner"], unique=False)
    op.add_column("prices", sa.Column("proof_id", sa.Integer(), nullable=True))
    op.create_foreign_key(None, "prices", "proofs", ["proof_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "prices", type_="foreignkey")
    op.drop_column("prices", "proof_id")
    op.drop_index(op.f("ix_proofs_owner"), table_name="proofs")
    op.drop_index(op.f("ix_proofs_mimetype"), table_name="proofs")
    op.drop_index(op.f("ix_proofs_id"), table_name="proofs")
    op.drop_index(op.f("ix_proofs_created"), table_name="proofs")
    op.drop_table("proofs")
    # ### end Alembic commands ###