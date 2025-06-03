# app/infrastructure/persistence/models_db/category_db_model.py
from app import db
import uuid
from sqlalchemy.orm import relationship

class CategoryDBModel(db.Model):
    __tablename__ = 'categories'

    category_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)

    products = relationship('ProductDBModel', back_populates='category')

    def __repr__(self):
        return f"<CategoryDBModel(id='{self.category_id}', name='{self.name}')>"