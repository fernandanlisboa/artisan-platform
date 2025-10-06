# app/infrastructure/persistence/models_db/product_db_model.py
from app.extensions import Base
from sqlalchemy import Numeric, Integer, DateTime, Column, String, Text, ForeignKey
import uuid
import datetime
from sqlalchemy.orm import relationship

class ProductDBModel(Base):
    __tablename__ = 'products'

    product_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    image_url = Column(String(255), nullable=True)
    registration_date = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String(20), nullable=False, default='active') # Ex: 'active', 'inactive', 'out_of_stock'

    # Foreign Keys
    artisan_id = Column(String(36), ForeignKey('artisans.artisan_id'), nullable=False)
    category_id = Column(String(36), ForeignKey('categories.category_id'), nullable=False)

    # Relationships
    artisan = relationship('ArtisanDBModel', back_populates='products')
    category = relationship('CategoryDBModel', back_populates='products')
    order_items = relationship('OrderItemDBModel', back_populates='product')
    reviews = relationship('ReviewDBModel', back_populates='product')
    cart_items = relationship('CartItemDBModel', back_populates='product')

    def __repr__(self):
        return f"<ProductDBModel(id='{self.product_id}', name='{self.name}')>"