# app/infrastructure/persistence/models_db/address_db_model.py
from app.extensions import Base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
import datetime
import uuid

class AddressDBModel(Base):
    """
    Database model for the Address entity.
    Maps to the 'addresses' table in MySQL as per the diagram.
    """
    __tablename__ = 'addresses'

    address_id = Column(String(36), primary_key=True, name='address_id', default=lambda: str(uuid.uuid4()))
    street = Column(String(255), nullable=False, name='street')
    number = Column(String(20), nullable=True, name='number')
    complement = Column(String(100), nullable=True, name='complement')
    neighborhood = Column(String(100), nullable=False, name='neighborhood')
    city = Column(String(100), nullable=False, name='city')
    state = Column(String(2), nullable=False, name='state')
    country = Column(String(100), nullable=False, default='Brasil', name='country')
    zip_code = Column(String(10), nullable=False, name='zip_code')

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships will be defined after all models are updated
    
    def __init__(self, street: str, number: str, 
                 neighborhood: str, city: str, state: str,
                 zip_code: str, country: str = 'Brasil', address_id: str = None, complement: str = None):
        if address_id is not None:
            self.address_id = address_id
        self.street = street
        self.number = number
        self.complement = complement
        self.neighborhood = neighborhood
        self.city = city
        self.state = state
        self.country = country
        self.zip_code = zip_code

    def __repr__(self):
        return f"<AddressDBModel(address_id='{self.address_id}', zip_code='{self.zip_code}', city='{self.city}')>"
