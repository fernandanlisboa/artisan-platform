from typing import Optional

class CategoryEntity:
    """
    Representa uma categoria de produtos no sistema.
    """

    def __init__(self, category_id: str, name: str, description: Optional[str] = None):
        """
        Inicializa uma nova instância de CategoryEntity.

        :param category_id: Identificador único da categoria.
        :param name: Nome da categoria.
        :param description: Descrição opcional da categoria.
        """
        self.category_id = category_id
        self.name = name
        self.description = description
    
    @classmethod
    def from_db_model(cls, db_model):
        return cls(
            category_id=db_model.category_id,
            name=db_model.name,
            description=db_model.description if db_model.description else None
        )
        
    def __repr__(self) -> str:
        return (f"CategoryEntity(category_id='{self.category_id}', "
                f"name='{self.name}', description='{self.description}')")
    
    def __str__(self) -> str:
        return f"Category: {self.name} (ID: {self.category_id}) - {self.description if self.description else 'No description'}"