# app/infrastructure/persistence/models_db/message_db_model.py
from app.extensions import Base
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import uuid
import datetime


class MessageDBModel(Base):
    __tablename__ = 'messages'

    message_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    content = Column(Text, nullable=False)
    send_date = Column(DateTime, default=datetime.datetime.utcnow)

    # Foreign Keys for Sender and Recipient (both are users)
    sender_user_id = Column(String(36), ForeignKey('users.user_id'), nullable=False)
    recipient_user_id = Column(String(36), ForeignKey('users.user_id'), nullable=False)
    
    # Foreign Key for Order (optional, if the message is linked to an order)
    order_id = Column(String(36), ForeignKey('orders.order_id'), nullable=True)

    # Relationship (sender and recipient are backref in UserDBModel)
    order = relationship('OrderDBModel', back_populates='messages')

    def __repr__(self):
        return f"<MessageDBModel(id='{self.message_id}', sender='{self.sender_user_id}')>"