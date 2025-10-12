# app/infrastructure/persistence/models_db/order_item_db_model.py
from app.extensions import Base
from sqlalchemy import Column, Integer, Numeric, String, Text, ForeignKey
import uuid
from sqlalchemy.orm import relationship

class OrderItemDBModel(Base):
    __tablename__ = 'order_items'

    order_item_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)

    # Foreign Keys
    product_id = Column(String(36), ForeignKey('products.product_id'), nullable=False)
    order_id = Column(String(36), ForeignKey('orders.order_id'), nullable=False)

    # Relationships
    product = relationship('ProductDBModel', back_populates='order_items')
    order = relationship('OrderDBModel', back_populates='order_items')

    def __repr__(self):
        return f"<OrderItemDBModel(id='{self.order_item_id}', product_id='{self.product_id}', order_id='{self.order_id}')>"