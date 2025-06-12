# app/infrastructure/persistence/models_db/user_db_model.py
from typing import Any
from app import db
import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import relationship # Import 'backref' for inverse relationships


class UserDBModel(db.Model):
    """
    Database model for the User entity.
    Maps to the 'users' table in MySQL as per the diagram.
    """
    __tablename__ = 'users' 

    user_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), name='user_id') # PK as per diagram
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False, name='password') # Stores password hash, original name 'senha'
    registration_date = db.Column(db.DateTime, default=datetime.now(timezone.utc), name='registration_date') # Original name 'data_cadastro'
    status = db.Column(db.String(20), nullable=False, default='active') # E.g., 'active', 'inactive', 'pending'

    # Foreign Key to Address (a user can have a primary address)
    address_id = db.Column(db.String(36), db.ForeignKey('addresses.address_id'), unique=False, nullable=True, name='address_id') # FK as per diagram
    
    # Relationship with AddressDBModel
    # 'uselist=False' implies a one-to-one or one-to-many from Address's perspective (one Address object for this User)
    # The 'backref' defines the inverse relationship from AddressDBModel back to UserDBModel
    # (e.g., address_obj.users_using_this_address will be a list of UserDBModel objects)
    address = relationship('AddressDBModel', back_populates='user', uselist=False) 

    # Relationships to BuyerDBModel and ArtisanDBModel
    # primaryjoin is crucial here as both Buyer and Artisan tables' PKs are also FKs to users.user_id
    # One User can be a Buyer OR an Artisan, but not both in the same "role" instance
    buyer = relationship('BuyerDBModel', back_populates='user', uselist=False, 
              primaryjoin="UserDBModel.user_id == BuyerDBModel.buyer_id")
    artisan = relationship('ArtisanDBModel', back_populates='user', uselist=False, 
                  primaryjoin="UserDBModel.user_id == ArtisanDBModel.artisan_id")

    # Relationships for Messages (sender and recipient are both UserDBModel instances)
    # foreign_keys specifies which FK column in MessageDBModel points back to this UserDBModel
    # backref defines the inverse relationships from MessageDBModel
    sent_messages = relationship('MessageDBModel', foreign_keys='[MessageDBModel.sender_user_id]', backref='sender_user')
    received_messages = relationship('MessageDBModel', foreign_keys='[MessageDBModel.recipient_user_id]', backref='recipient_user')
    
    # --- Método __init__ (Essencial!) ---
    def __init__(self, email: str, password_hash: str, status: str = 'active', 
                 user_id: str = None, registration_date: datetime = None,
                 address_id: str = None):  # Adicionado address_id
        if user_id is not None:
            self.user_id = user_id
        self.email = email
        self.password_hash = password_hash
        # self.role = role  # Remover esta linha, role não existe nos parâmetros
        self.status = status
        self.registration_date = registration_date if registration_date else datetime.now(timezone.utc)
        self.address_id = address_id  # Adicionado address_id
        
    def __repr__(self):
        return f"<UserDBModel(user_id='{self.user_id}', email='{self.email}')>"
    
    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)