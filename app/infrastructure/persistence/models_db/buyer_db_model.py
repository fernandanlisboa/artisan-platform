# app/infrastructure/persistence/models_db/buyer_db_model.py
from app import db
from sqlalchemy.orm import relationship

class BuyerDBModel(db.Model):
    __tablename__ = 'buyers'

    buyer_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), primary_key=True) # PK is also FK
    full_name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=True)

    user = relationship('UserDBModel', back_populates='buyer')
    orders = relationship('OrderDBModel', back_populates='buyer')
    reviews = relationship('ReviewDBModel', back_populates='buyer')

    def __repr__(self):
        return f"<BuyerDBModel(id='{self.buyer_id}', name='{self.full_name}')>"