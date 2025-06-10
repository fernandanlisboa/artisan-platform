# app/infrastructure/persistence/address_repository_impl.py
from app.domain.repositories.address_repository_interface import IAddressRepository
from app.infrastructure.persistence.models_db.address_db_model import AddressDBModel
from app.domain.models.address import AddressEntity as Address # Importa a entidade de domínio pura Address
from app import db # Acesso à instância global do SQLAlchemy
from typing import Optional

class AddressRepository(IAddressRepository):
    """
    Concrete implementation of AddressRepository using Flask-SQLAlchemy.
    Handles persistence operations for AddressDBModel.
    """
    def save(self, address_entity: Address) -> Address: # Aceita Address (entidade pura)
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
        try:
            db.session.add(address_db_model)
            db.session.commit()
        except Exception as e:
            print(f"Error saving address: {e}")
            db.session.rollback()
            raise
        
        address_entity.address_id = address_db_model.address_id  # Atualiza o ID da entidade pura com o ID gerado pelo banco
        print("Address Entity after save: ", address_entity)
        return address_entity # Retorna a entidade pura que foi salva
    
    def get_by_id(self, address_id: str) -> Optional[Address]: # Retorna Entidade de Domínio Pura
        """Gets an Address by ID and converts it to a pure domain entity."""
        address_db_model = AddressDBModel.query.get(address_id)
        if address_db_model:
            return Address(
                address_id=address_db_model.address_id,
                street=address_db_model.street,
                number=address_db_model.number,
                complement=address_db_model.complement,
                neighborhood=address_db_model.neighborhood,
                city=address_db_model.city,
                state=address_db_model.state,
                country=address_db_model.country,
                zip_code=address_db_model.zip_code
            )
        return None
    
    def get_by_attributes(self, address_entity: Address) -> Optional[Address]:
        """Gets an Address entity by its attributes."""
        filter_criteria = address_entity.to_filter_dict()
        query = AddressDBModel.query.filter_by(**filter_criteria)
        address_db_model = query.first()
        if address_db_model:
            return Address(
                address_id=address_db_model.address_id,
                street=address_db_model.street,
                number=address_db_model.number,
                complement=address_db_model.complement,
                neighborhood=address_db_model.neighborhood,
                city=address_db_model.city,
                state=address_db_model.state,
                country=address_db_model.country,
                zip_code=address_db_model.zip_code
            )
        return None
