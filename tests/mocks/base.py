from abc import ABC, abstractmethod
from faker import Faker

# Singleton para acesso ao Faker
class FakerInstance:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Faker('pt_BR')  # Use a localização apropriada
        return cls._instance

# Interface base para todas as entidades mock
class BaseMockEntity(ABC):
    """Classe base para todas as entidades mock."""
    
    @classmethod
    def to_dict(cls, entity):
        """Converte uma entidade em dicionário."""
        return {k: v for k, v in entity.__dict__.items() 
                if not k.startswith('_') and not callable(v)}

# Interface base para as factories
class AbstractEntityFactory(ABC):
    """Interface para as factories de entidades."""
    
    @abstractmethod
    def create(self, **kwargs):
        """Cria uma instância da entidade."""
        pass
        
    @abstractmethod
    def create_many(self, count, **kwargs):
        """Cria múltiplas instâncias da entidade."""
        pass

# Interface base para builders
class EntityBuilder(ABC):
    """Interface para builders de entidades."""
    
    def __init__(self):
        self.reset()
    
    @abstractmethod
    def reset(self):
        """Reinicia o builder para o estado inicial."""
        pass
    
    @abstractmethod
    def build(self):
        """Constrói e retorna a entidade configurada."""
        pass