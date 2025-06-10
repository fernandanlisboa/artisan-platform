# app/infrastructure/persistence/models_db/product_db_model.py
from app import db
import uuid
import datetime
from sqlalchemy.orm import relationship

class ProductDBModel(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    image_url = db.Column(db.String(255), nullable=True)
    registration_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='active') # Ex: 'active', 'inactive', 'out_of_stock'

    # Foreign Keys
    artisan_id = db.Column(db.String(36), db.ForeignKey('artisans.artisan_id'), nullable=False)
    category_id = db.Column(db.String(36), db.ForeignKey('categories.category_id'), nullable=False)

    # Relationships
    artisan = relationship('ArtisanDBModel', back_populates='products')
    category = relationship('CategoryDBModel', back_populates='products')
    order_items = relationship('OrderItemDBModel', back_populates='product')
    reviews = relationship('ReviewDBModel', back_populates='product')
    cart_items = relationship('CartItemDBModel', back_populates='product')

    def __repr__(self):
        return f"<ProductDBModel(id='{self.product_id}', name='{self.name}')>"