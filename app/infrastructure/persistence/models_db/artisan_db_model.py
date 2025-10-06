# app/infrastructure/persistence/models_db/artisan_db_model.py
from app.extensions import Base
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
import datetime

class ArtisanDBModel(Base):
    __tablename__ = 'artisans'

    artisan_id = Column(String(36), ForeignKey('users.user_id'), primary_key=True) # PK is also FK
    store_name = Column(String(255), nullable=False)
    bio = Column(Text, nullable=True)
    phone = Column(String(20), nullable=True)
    status = Column(String(20), nullable=False, default='active') # Ex: 'active', 'pending', 'suspended'

    user = relationship('UserDBModel', back_populates='artisan')
    products = relationship('ProductDBModel', back_populates='artisan')

    def __init__(self, artisan_id, store_name, bio=None, phone=None, status='active'):
        self.artisan_id = artisan_id
        self.store_name = store_name
        self.bio = bio
        self.phone = phone
        self.status = status
    def __repr__(self):
        return f"<ArtisanDBModel(id='{self.artisan_id}', store='{self.store_name}')>"
    