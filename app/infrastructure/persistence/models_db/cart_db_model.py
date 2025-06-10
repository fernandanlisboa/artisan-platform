from app import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

class CartDBModel(db.Model):
    """
    Modelo ORM para a tabela 'carts'.
    Representa o carrinho de compras de um usuário.
    """
    __tablename__ = 'carts'

    # Colunas da tabela
    cart_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Chave Estrangeira para o usuário.
    # Um usuário tem um carrinho, então a relação é única.
    buyer_id = db.Column(db.String(36), db.ForeignKey('buyers.buyer_id'), nullable=False)
    
    # Timestamps para controle
    # server_default é executado pelo próprio banco de dados, o que é ótimo para consistência.
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    # --- RELACIONAMENTOS ---
    
    # 1. Relação com User: Permite acessar o objeto User a partir do carrinho (ex: meu_carrinho.user)
    #    'back_populates' cria a relação inversa no modelo User.
    buyer = relationship('BuyerDBModel', back_populates='cart')


    # 2. Relação com CartItem (O lado "Um" da relação Um-para-Muitos)
    #    Isso cria o atributo 'meu_carrinho.items', que retorna uma LISTA de objetos CartItem.
    #    'cascade' é a instrução mais importante aqui:
    #       - 'all': Aplica todas as operações (como salvar) em cascata.
    #       - 'delete-orphan': Se um CartItem for removido da lista 'cart.items' no código,
    #         ele será deletado do banco. Se o Cart for deletado, todos os seus CartItems
    #         serão deletados juntos. Essencial para a integridade do carrinho.
    items = relationship('CartItemDBModel', back_populates='cart', cascade='all, delete-orphan')

    # Construtor corrigido
    def __init__(self, buyer_id: str, cart_id: str = None):
        if cart_id is not None:
            self.cart_id = cart_id
        self.buyer_id = buyer_id
    
    def __repr__(self):
        return f"<CartDBModel(cart_id='{self.cart_id}', buyer_id='{self.buyer_id}')>"