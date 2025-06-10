# app/infrastructure/persistence/models_db/order_db_model.py
from app import db
import uuid
import datetime
from sqlalchemy.orm import relationship

class OrderDBModel(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    order_status = db.Column(db.String(50), nullable=False, default='pending') # Ex: 'pending', 'processing', 'shipped', 'delivered', 'canceled'
    total_value = db.Column(db.Numeric(10, 2), nullable=False)
    
    # The diagram shows 'delivery_address' as a direct field, not FK to Address
    # Assuming it's a string for this specific order
    delivery_address_id = db.Column(db.String(36), db.ForeignKey('addresses.address_id'), unique=True, nullable=True, name='address_id')
    delivery_address = relationship('AddressDBModel') 

    payment_method = db.Column(db.String(50), nullable=False)
    gateway_transaction_id = db.Column(db.String(255), nullable=True)

    # Foreign Key
    buyer_id = db.Column(db.String(36), db.ForeignKey('buyers.buyer_id'), nullable=False)

    # Relationships
    buyer = relationship('BuyerDBModel', back_populates='orders')
    order_items = relationship('OrderItemDBModel', back_populates='order')
    messages = relationship('MessageDBModel', back_populates='order')

    def __repr__(self):
        return f"<OrderDBModel(id='{self.order_id}', buyer_id='{self.buyer_id}', total='{self.total_value}')>"