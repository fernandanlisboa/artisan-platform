from app import db
from sqlalchemy.sql import func
import uuid

from sqlalchemy.orm import relationship

class CartItemDBModel(db.Model):
    __tablename__ = 'cart_items'

    # Colunas da tabela
    cart_item_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    quantity = db.Column(db.Integer, nullable=False, default=1)
    
    # Chave Estrangeira que aponta para o ID do carrinho ao qual este item pertence.
    # Este é o elo que estabelece a relação.
    cart_id = db.Column(db.String(36), db.ForeignKey('carts.cart_id'), nullable=False)
    
    # Chave Estrangeira que aponta para o ID do produto que foi adicionado.
    product_id = db.Column(db.String(36), db.ForeignKey('products.product_id'), nullable=False)
    
    # --- RELACIONAMENTOS ---

    # 1. Relação com Cart (O lado "Muitos" da relação)
    #    Isso cria o atributo 'meu_item.cart', que retorna UM ÚNICO objeto Cart.
    #    'back_populates' liga esta relação ao atributo 'items' no modelo Cart.
    cart = relationship('CartDBModel', back_populates='items')  # Não 'Cart'

    # 2. Relação com Product
    #    Permite acessar facilmente os detalhes do produto a partir do item do carrinho
    #    (ex: meu_item.product.name, meu_item.product.price)
    product = relationship('ProductDBModel')  # Não 'Product'
    
    def __init__(self, cart_id: str, product_id: str, quantity: int = 1, cart_item_id: str = None):
        if cart_item_id is not None:
            self.cart_item_id = cart_item_id
        self.cart_id = cart_id
        self.product_id = product_id
        self.quantity = quantity