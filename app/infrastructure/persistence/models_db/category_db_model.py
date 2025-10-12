from app.extensions import Base
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
import uuid


class CategoryDBModel(Base):
    __tablename__ = 'categories'

    category_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

    products = relationship('ProductDBModel', back_populates='category')
    
    def __init__(self, name, description=None, category_id=None):
        """
        Initializes a new CategoryDBModel instance.
        
        :param name: The name of the category.
        :param description: A brief description of the category.
        :param category_id: Optional unique identifier for the category.
        """
        self.category_id = category_id or str(uuid.uuid4())
        self.name = name
        self.description = description

    @classmethod
    def from_entity(cls, category_entity):
        """
        Converts a domain entity to a database model instance.
        """
        return cls(
            category_id=category_entity.category_id,
            name=category_entity.name,
            description=category_entity.description
        )

    def __repr__(self):
        return f"<CategoryDBModel(id='{self.category_id}', name='{self.name}')>"