from pydantic import BaseModel, Field
from typing import Optional
from app.domain.models.user import UserEntity as User
"""
Propósito: Definir os formatos de dados para a comunicação com o exterior.
Lógica: Conterá a classe RegisterArtisanRequest (um Pydantic BaseModel) que 
descreve os campos esperados no corpo da requisição POST 
(e-mail, senha, nome da loja, telefone, bio). 
Ela fará a validação de formato e presença dos campos 
(ex: e-mail válido, string não vazia). 
Terá também a classe UserResponse para formatar a resposta de sucesso.
"""

class RegisterArtisanRequest(BaseModel):
    email: str = Field(..., example="artisan@example.com", max_length=120)
    password: str = Field(..., min_length=8, max_length=64)
    store_name: str = Field(..., example="Artisan's Workshop", max_length=255)
    phone: Optional[str] = Field(None, example="71999999999", max_length=20)
    bio: Optional[str] = Field(None, example="We create handmade jewelry.", max_length=1000)

class UserResponse(BaseModel):
    """DTO for user response (e.g., after registration)."""
    user_id: str = Field(..., alias='user_id') # Maps 'user_id' from entity/model to 'user_id' in response
    email: str
    role: str
    status: str
    
    class Config:
        # orm_mode = True é útil se estiver mapeando diretamente de um modelo ORM.
        # Mas como estamos usando uma entidade de domínio pura, from_domain_entity é mais explícito.
        # allow_population_by_field_name = True é útil para Pydantic preencher campos por alias.
        pass 

    @classmethod
    def from_domain_entity(cls, user_entity: User):
        """Helper to create DTO from a pure domain User entity."""
        return cls(
            user_id=user_entity.user_id,
            email=user_entity.email,
            role=user_entity.role,
            status=user_entity.status
        )