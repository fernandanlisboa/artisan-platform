# app/infrastructure/persistence/models_db/review_db_model.py
from app.extensions import Base
from sqlalchemy import Integer, Column, DateTime, String, Text, ForeignKey
import uuid
import datetime
from sqlalchemy.orm import relationship

class ReviewDBModel(Base):
    __tablename__ = 'reviews'

    review_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    rating = Column(Integer, nullable=False) # 1 to 5
    comment = Column(Text, nullable=True)
    review_date = Column(DateTime, default=datetime.datetime.utcnow)

    # Foreign Keys
    buyer_id = Column(String(36), ForeignKey('buyers.buyer_id'), nullable=False)
    product_id = Column(String(36), ForeignKey('products.product_id'), nullable=False)

    # Relationships
    buyer = relationship('BuyerDBModel', back_populates='reviews')
    product = relationship('ProductDBModel', back_populates='reviews')

    def __repr__(self):
        return f"<ReviewDBModel(id='{self.review_id}', product_id='{self.product_id}', rating='{self.rating}')>"