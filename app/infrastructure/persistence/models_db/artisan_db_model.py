# app/infrastructure/persistence/models_db/artisan_db_model.py
from app import db
import datetime
from sqlalchemy.orm import relationship

class ArtisanDBModel(db.Model):
    __tablename__ = 'artisans'

    artisan_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), primary_key=True) # PK is also FK
    store_name = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='active') # Ex: 'active', 'pending', 'suspended'

    user = relationship('UserDBModel', back_populates='artisan')
    products = relationship('ProductDBModel', back_populates='artisan')

    def __repr__(self):
        return f"<ArtisanDBModel(id='{self.artisan_id}', store='{self.store_name}')>"