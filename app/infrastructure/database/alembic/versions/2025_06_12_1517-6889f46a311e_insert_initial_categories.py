"""insert initial categories

Revision ID: 6889f46a311e
Revises: 3f6549aaf2af
Create Date: 2025-06-12 15:17:19.647049

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import uuid


# revision identifiers, used by Alembic.
revision: str = '6889f46a311e'
down_revision: Union[str, None] = '3f6549aaf2af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Insert new categories."""
    ceramic_category_id = str(uuid.uuid4())
    textil_category_id = str(uuid.uuid4())
    costume_jwelry_category_id = str(uuid.uuid4())
    wood_category_id = str(uuid.uuid4())

    op.bulk_insert(
        sa.Table(
            'categories',
            sa.MetaData(),
            sa.Column('category_id', sa.String(length=36), primary_key=True),
            sa.Column('name', sa.String(length=100), nullable=False),
            sa.Column('description', sa.String(length=255), nullable=True)
        ),
        [
            {
                'category_id': ceramic_category_id,
                'name': 'Cerâmica',
                'description': 'Produtos de cerâmica feitos à mão, como vasos, pratos e utensílios decorativos.'
            },
            {
                'category_id': textil_category_id,
                'name': 'Têxtil',
                'description': 'Produtos têxteis artesanais, incluindo roupas, acessórios e itens de decoração.'
            },
            {
                'category_id': costume_jwelry_category_id,
                'name': 'Bijuterias',
                'description': 'Bijuterias artesanais, incluindo colares, brincos e pulseiras.'
            },
            {
                'category_id': wood_category_id,
                'name': 'Madeira',
                'description': 'Produtos de madeira feitos à mão, como móveis, brinquedos e utensílios decorativos.'
            }
        ]
    )
    
def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM categories WHERE nome IN ('Cerâmica', 'Têxtil', 'Bijuteria', 'Madeira');")
