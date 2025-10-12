# app/infrastructure/persistence/models_db/buyer_db_model.py
from app.extensions import Base
from sqlalchemy import Column, String, ForeignKey  
from sqlalchemy.orm import relationship

class BuyerDBModel(Base):
    __tablename__ = 'buyers'

    buyer_id = Column(String(36), ForeignKey('users.user_id'), primary_key=True) # PK is also FK
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)

    user = relationship('UserDBModel', back_populates='buyer')
    orders = relationship('OrderDBModel', back_populates='buyer')
    reviews = relationship('ReviewDBModel', back_populates='buyer')
    cart = relationship('CartDBModel', back_populates='buyer', uselist=False)
    
    def __repr__(self):
        return f"<BuyerDBModel(id='{self.buyer_id}', name='{self.full_name}')>"