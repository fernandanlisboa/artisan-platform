# app/infrastructure/persistence/models_db/review_db_model.py
from app import db
import uuid
import datetime
from sqlalchemy.orm import relationship

class ReviewDBModel(db.Model):
    __tablename__ = 'reviews'

    review_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    rating = db.Column(db.Integer, nullable=False) # 1 to 5
    comment = db.Column(db.Text, nullable=True)
    review_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # Foreign Keys
    buyer_id = db.Column(db.String(36), db.ForeignKey('buyers.buyer_id'), nullable=False)
    product_id = db.Column(db.String(36), db.ForeignKey('products.product_id'), nullable=False)

    # Relationships
    buyer = relationship('BuyerDBModel', back_populates='reviews')
    product = relationship('ProductDBModel', back_populates='reviews')

    def __repr__(self):
        return f"<ReviewDBModel(id='{self.review_id}', product_id='{self.product_id}', rating='{self.rating}')>"