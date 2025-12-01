"""usuarios adicionais

Revision ID: 18d2726ebaad
Revises: 314c21e167c2
Create Date: 2025-11-30 22:20:41.523781

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '18d2726ebaad'
down_revision: Union[str, Sequence[str], None] = '314c21e167c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
# Defina os valores do enum (exatamente como estão no banco atualmente)
enum_values = ('DECLARANTE', 'VITIMA', 'AUTOR', 'SUSPEITO', 'TESTEMUNHA', 'OUTRO')

def upgrade() -> None:
    # Usar batch para operações que o SQLite não suporta diretamente
    with op.batch_alter_table('declarante', schema=None) as batch_op:
        batch_op.alter_column(
            'tipo_envolvimento',
            existing_type=sa.VARCHAR(length=27),
            type_=sa.Enum(*enum_values, name='tipoenvolvimento'),
            existing_nullable=False,
            postgresql_using='tipo_envolvimento::tipoenvolvimento'  # só tem efeito no PostgreSQL
        )


def downgrade() -> None:
    with op.batch_alter_table('declarante', schema=None) as batch_op:
        batch_op.alter_column(
            'tipo_envolvimento',
            existing_type=sa.Enum(*enum_values, name='tipoenvolvimento'),
            type_=sa.VARCHAR(length=27),
            existing_nullable=False
        )
