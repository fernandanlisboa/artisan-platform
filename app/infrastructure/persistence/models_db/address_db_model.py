# app/infrastructure/persistence/models_db/address_db_model.py
from app import db
import uuid
import datetime

class AddressDBModel(db.Model):
    """
    Database model for the Address entity.
    Maps to the 'addresses' table in MySQL as per the diagram.
    """
    __tablename__ = 'addresses'

    address_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), name='address_id') # PK as per diagram
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

    def __repr__(self):
        return f"<AddressDBModel(address_id='{self.address_id}', zip_code='{self.zip_code}', city='{self.city}')>"