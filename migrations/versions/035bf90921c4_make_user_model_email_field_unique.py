"""make user model email field unique

Revision ID: 035bf90921c4
Revises: ac7a14c4c5aa
Create Date: 2024-10-28 19:48:48.210406

"""

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "035bf90921c4"
down_revision: str | None = "ac7a14c4c5aa"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, "users", ["email"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "users", type_="unique")
    # ### end Alembic commands ###
