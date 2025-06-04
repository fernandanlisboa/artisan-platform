# app/infrastructure/persistence/models_db/message_db_model.py
from app import db
import uuid
import datetime
from sqlalchemy.orm import relationship

class MessageDBModel(db.Model):
    __tablename__ = 'messages'

    message_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    content = db.Column(db.Text, nullable=False)
    send_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # Foreign Keys for Sender and Recipient (both are users)
    sender_user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    recipient_user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    
    # Foreign Key for Order (optional, if the message is linked to an order)
    order_id = db.Column(db.String(36), db.ForeignKey('orders.order_id'), nullable=True)

    # Relationship (sender and recipient are backref in UserDBModel)
    order = relationship('OrderDBModel', back_populates='messages')

    def __repr__(self):
        return f"<MessageDBModel(id='{self.message_id}', sender='{self.sender_user_id}')>"