from abc import ABC, abstractmethod
from app.domain.models.artisan import ArtisanEntity

#interface
class IArtisanRepository(ABC):
    
    @abstractmethod
    def save(self, artisan_entity: ArtisanEntity) -> ArtisanEntity: # Aceita e retorna a entidade pura
        pass