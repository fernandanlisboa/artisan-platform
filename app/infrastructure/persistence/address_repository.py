# app/infrastructure/persistence/address_repository_impl.py
from app.domain.repositories.address_repository_interface import IAddressRepository
from app.infrastructure.persistence.models_db.address_db_model import AddressDBModel
from app.domain.models.address import AddressEntity as Address # Importa a entidade de domínio pura Address
from app.extensions import SessionLocal
from typing import Optional

class AddressRepository(IAddressRepository):
    """
    Concrete implementation of AddressRepository using Flask-SQLAlchemy.
    Handles persistence operations for AddressDBModel.
    """
    def create(self, address_entity: Address) -> Address: # Aceita Address (entidade pura)
        """Saves an Address entity to the database by converting it to AddressDBModel."""
        # CONVERSÃO: Entidade de Domínio Pura -> Modelo ORM
        address_db_model = AddressDBModel(
            street=address_entity.street,
            number=address_entity.number,
            complement=address_entity.complement,
            neighborhood=address_entity.neighborhood,
            city=address_entity.city,
            state=address_entity.state,
            country=address_entity.country,
            zip_code=address_entity.zip_code
        )
        print("Address DB Model: ", address_db_model)
        session = SessionLocal()
        try:
            session.add(address_db_model)
            session.commit()
            address_entity.address_id = address_db_model.address_id  # Atualiza o ID da entidade pura com o ID gerado pelo banco
        except Exception as e:
            print(f"Error saving address: {e}")
            session.rollback()
            raise
        finally:
            session.close()
        
        print("Address Entity after save: ", address_entity)
        return address_entity # Retorna a entidade pura que foi salva
    
    def get_by_id(self, address_id: str) -> Optional[Address]:
        """Gets an Address by ID and converts it to a pure domain entity."""
        session = SessionLocal()
        try:
            address_db_model = session.get(AddressDBModel, address_id)
            if address_db_model:
                return Address.from_db_model(address_db_model)
            return None
        finally:
            session.close()
    
    def get_by_attributes(self, address_entity: Address) -> Optional[Address]:
        """Gets an Address entity by its attributes."""
        filter_criteria = address_entity.to_filter_dict()
        session = SessionLocal()
        try:
            address_db_model = session.query(AddressDBModel).filter_by(**filter_criteria).first()
            if address_db_model:
                return Address.from_db_model(address_db_model)
            return None
        finally:
            session.close()
