from abc import ABC, abstractmethod
from app.domain.models.artisan import ArtisanEntity

#interface
class IArtisanRepository(ABC):
    
    @abstractmethod
    def create(self, artisan_entity: ArtisanEntity) -> ArtisanEntity: # Aceita e retorna a entidade pura
        pass
    
    @abstractmethod
    def get_artisan_by_id(self, artisan_id: str):
        """
        Retrieves an Artisan entity by its ID.
        Converts the ORM model to a pure domain entity.
        """
        pass