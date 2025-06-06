# app/domain/repositories/address_repository.py
from abc import ABC, abstractmethod
from typing import Optional
from app.domain.models.address import AddressEntity # Importa a entidade de domínio pura Address

class IAddressRepository(ABC):
    """
    Interface (Abstract Base Class) for Address data access operations.
    Defines the contract for interacting with the 'addresses' table.
    """
    @abstractmethod
    def save(self, address: AddressEntity) -> AddressEntity:
        """Saves an Address entity to the persistent storage."""
        pass

    @abstractmethod
    def get_by_id(self, address_id: str) -> Optional[AddressEntity]:
        """Gets an Address entity by its ID."""
        pass