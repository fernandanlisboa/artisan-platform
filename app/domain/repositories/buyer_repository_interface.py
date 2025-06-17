from abc import ABC, abstractmethod
from app.domain.models.buyer import BuyerEntity

#interface
class IBuyerRepository(ABC):
    
    @abstractmethod
    def create(self, buyer_entity: BuyerEntity) -> BuyerEntity: # Aceita e retorna a entidade pura
        pass