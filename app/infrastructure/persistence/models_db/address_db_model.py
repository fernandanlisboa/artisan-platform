# app/infrastructure/persistence/models_db/address_db_model.py
from app import db
import datetime
from sqlalchemy.orm import relationship
import uuid
class AddressDBModel(db.Model):
    """
    Database model for the Address entity.
    Maps to the 'addresses' table in MySQL as per the diagram.
    """
    __tablename__ = 'addresses'

    address_id = db.Column(db.String(36), primary_key=True, name='address_id', default=lambda: str(uuid.uuid4())) # PK as per diagram
    street = db.Column(db.String(255), nullable=False, name='street') # Street name/public place
    number = db.Column(db.String(20), nullable=True, name='number') # House/building number
    complement = db.Column(db.String(100), nullable=True, name='complement') # Complementary address info (e.g., apartment number)
    neighborhood = db.Column(db.String(100), nullable=False, name='neighborhood') # Neighborhood
    city = db.Column(db.String(100), nullable=False, name='city') # City
    state = db.Column(db.String(2), nullable=False, name='state') # State abbreviation (e.g., 'BA', 'SP')
    country = db.Column(db.String(100), nullable=False, default='Brasil', name='country') # Country
    zip_code = db.Column(db.String(10), nullable=False, name='zip_code') # Postal code (ZIP)

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    user = relationship('UserDBModel', back_populates='address', uselist=False)
    
    def __init__(self, street: str, number: str, 
                 neighborhood: str, city: str, state: str,
                 zip_code: str, country: str = 'Brasil', address_id: str = None, complement: str = None):
        if not address_id is None:
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
