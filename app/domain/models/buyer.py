from app.domain.models.user import UserEntity 
from typing import Optional

class BuyerEntity(UserEntity):
    """
    Representa um usuário comprador no sistema, com atributos específicos do comprador.
    Herda de UserEntity para incluir atributos de usuário comuns como user_id, email, password, status, e address_id.
    """

    def __init__(self, buyer_id: str, full_name: str, phone: Optional[str] = None):
        """
        Inicializa uma nova instância de BuyerEntity.
        O buyer_id deve ser o mesmo que o user_id da UserEntity correspondente.
        """
        self.buyer_id = buyer_id
        self.full_name = full_name
        self.phone = phone        

    def __repr__(self):
        return (f"BuyerEntity(buyer_id='{self.buyer_id}', full_name='{self.full_name}'"
                f"phone='{self.phone}')")