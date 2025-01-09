"""agregando columnas a providers

Revision ID: 1918bacafc20
Revises: b80ca775132b
Create Date: 2025-01-01 10:07:34.786574

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1918bacafc20'
down_revision: Union[str, None] = 'b80ca775132b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('provider', sa.Column('email', sa.sql.sqltypes.String(), nullable=True))
    op.add_column('provider', sa.Column('phone', sa.sql.sqltypes.String(), nullable=True))
    op.add_column('provider', sa.Column('address', sa.sql.sqltypes.String(), nullable=True))
    op.drop_column('provider', 'contact_info')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('provider', sa.Column('contact_info', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('provider', 'address')
    op.drop_column('provider', 'phone')
    op.drop_column('provider', 'email')
    # ### end Alembic commands ###