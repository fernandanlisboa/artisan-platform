from pydantic import BaseModel, Field, EmailStr  # Importar EmailStr
from typing import Optional
from datetime import datetime
from app.domain.models.artisan import ArtisanEntity
from app.domain.models.buyer import BuyerEntity 
from app.domain.models.user import UserEntity
from app.domain.models.address import AddressEntity
"""
Propósito: Definir os formatos de dados para a comunicação com o exterior.
Lógica: Conterá a classe RegisterArtisanRequest (um Pydantic BaseModel) que 
descreve os campos esperados no corpo da requisição POST 
(e-mail, senha, nome da loja, telefone, bio). 
Ela fará a validação de formato e presença dos campos 
(ex: e-mail válido, string não vazia). 
Terá também a classe UserResponse para formatar a resposta de sucesso.
"""

# --- DTO para a Requisição de Endereço (Permanece o mesmo) ---
class RegisterAddressRequest(BaseModel):
    """DTO for address registration or update requests."""
    street: str = Field(..., example="Rua das Flores", max_length=255)
    number: Optional[str] = Field(None, example="123", max_length=20) 
    complement: Optional[str] = Field(None, example="Apto 101", max_length=100)
    neighborhood: str = Field(..., example="Centro", max_length=100)
    city: str = Field(..., example="Salvador", max_length=100)
    state: str = Field(..., example="BA", max_length=2) 
    zip_code: str = Field(..., example="40000-000", max_length=10) 
    country: Optional[str] = Field("Brasil", example="Brasil", max_length=100)

# --- DTO para a Requisição de Registro de Artesão (AGORA COM ENDEREÇO ANINHADO) ---
class RegisterArtisanRequest(BaseModel):
    """DTO for artisan registration request, now with optional nested address."""
    email: str = Field(..., example="artisan@example.com", max_length=120)
    password: str = Field(..., min_length=8, max_length=64)
    store_name: str = Field(..., example="Artisan's Workshop", max_length=255)
    phone: Optional[str] = Field(None, example="71999999999", max_length=20)
    bio: Optional[str] = Field(None, example="We create handmade jewelry.", max_length=1000)
    
    # --- NOVO: Campo de Endereço Aninhado ---
    # Optional, pois um artesão pode se registrar sem fornecer o endereço principal neste momento
    address: RegisterAddressRequest = Field(None, description="primary address details for the artisan.")

class AddressResponse(BaseModel):
    address_id: str = Field(..., example="a1b2c3d4-e5f6-7890-1234-567890abcdef")
    street: str = Field(..., example="Rua das Palmeiras")
    number: Optional[str] = Field(None, example="123A")
    complement: Optional[str] = Field(None, example="Apto 4B")
    neighborhood: str = Field(..., example="Centro")
    city: str = Field(..., example="Cidade das Artes")
    state: str = Field(..., example="BA")
    zip_code: str = Field(..., example="40000-000")
    country: str = Field("Brasil", example="Brasil")

    class Config:
        from_attributes = True # Útil se você for popular diretamente de um AddressDBModel
                        # ou se sua AddressEntity tiver atributos compatíveis
# DTO para a Resposta do Registro de Artesão
class ArtisanRegistrationResponse(BaseModel):
    user_id: str = Field(..., description="ID único do usuário/artesão.", example="u1b2c3d4-e5f6-7890-1234-567890abcdef")
    email: str = Field(..., description="Email do artesão.", example="artesao@email.com")
    store_name: str = Field(..., description="Nome da loja/ateliê do artesão.", example="Ateliê Mãos de Ouro")
    phone: Optional[str] = Field(None, description="Telefone de contato do artesão.", example="71999998888")
    bio: Optional[str] = Field(None, description="Biografia ou descrição do artesão.", example="Crio peças únicas em cerâmica.")

    status: str = Field(..., description="Status atual do usuário.", example="active")
 
    address: Optional[AddressResponse] = Field(None, description="Endereço principal do artesão.")

    class Config:
        # from_attributes = True pode ser útil se você estiver construindo este DTO
        # diretamente de modelos ORM
        pass

    # Método para criar o DTO a partir de suas entidades de domínio
    # Você precisará adaptar isso com base em como suas entidades UserEntity, ArtisanEntity, e AddressEntity estão estruturadas
    # e como elas se relacionam.
    # Vamos supor que você tenha uma ArtisanEntity que contém ou tem acesso a UserEntity e AddressEntity.

    @classmethod
    def from_domain_entities(cls, artisan_entity: ArtisanEntity, user_entity: UserEntity, address_entity: Optional[AddressEntity]):
        """
        Cria o DTO a partir das entidades de domínio.
        'ArtisanEntity', 'UserEntity', 'AddressEntity' são placeholders para suas classes de entidade.
        """
        
        address_response_data = None
        if address_entity and address_entity.address_id:
            address_response_data = AddressResponse(
                address_id=address_entity.address_id,
                street=address_entity.street,
                number=address_entity.number,
                complement=address_entity.complement,
                neighborhood=address_entity.neighborhood,
                city=address_entity.city,
                state=address_entity.state,
                zip_code=address_entity.zip_code,
                country=address_entity.country
            )
            
        return cls(
            user_id=user_entity.user_id, # que também é o artisan_entity.artisan_id
            email=user_entity.email,
            store_name=artisan_entity.store_name, # "nome do artesão"
            phone=artisan_entity.phone,
            bio=artisan_entity.bio,
            status=user_entity.status,
            address=address_response_data,
            registration_date=user_entity.registration_date
        )
 
class RegisterBuyerRequest(BaseModel):
    """DTO para a requisição de registro de um comprador, com endereço aninhado."""
    email: EmailStr = Field(...)  # EmailStr faz validação automática
    password: str = Field(..., min_length=8, max_length=64)
    full_name: str = Field(..., example="João da Silva", max_length=255) # Alterado para full_name
    phone: Optional[str] = Field(None, example="71988887777", max_length=20)

    address: RegisterAddressRequest = Field(..., description="Detalhes do endereço principal do comprador.")


# --- DTO para a Resposta do Registro de Comprador ---
class BuyerRegistrationResponse(BaseModel):
    user_id: str = Field(..., description="ID único do usuário/comprador.", example="u1b2c3d4-e5f6-7890-1234-567890abcdef")
    email: str = Field(..., description="Email do comprador.", example="comprador@email.com")
    full_name: str = Field(..., description="Nome completo do comprador.", example="Maria de Souza") # Alterado para full_name
    phone: Optional[str] = Field(None, description="Telefone de contato do comprador.", example="71999991111")
    status: str = Field(..., description="Status atual do usuário.", example="active")
    registration_date: Optional[datetime] = Field(..., description="Data de registro do usuário.", example="2023-05-30T14:30:00")
    address: Optional[AddressResponse] = Field(None, description="Endereço principal do comprador.")

    class Config:
        pass

    @classmethod
    def from_domain_entities(cls, buyer_entity: BuyerEntity, user_entity: UserEntity, address_entity: Optional[AddressEntity]):
        """
        Cria o DTO a partir das entidades de domínio.
        """
        address_response_data = None
        if address_entity and address_entity.address_id:
            address_response_data = AddressResponse(
                address_id=address_entity.address_id,
                street=address_entity.street,
                number=address_entity.number,
                complement=address_entity.complement,
                neighborhood=address_entity.neighborhood,
                city=address_entity.city,
                state=address_entity.state,
                zip_code=address_entity.zip_code,
                country=address_entity.country
            )

        return cls(
            user_id=user_entity.user_id, # O ID do comprador é o mesmo ID do usuário
            email=user_entity.email,
            full_name=buyer_entity.full_name, # Alterado para full_name
            phone=buyer_entity.phone,
            status=user_entity.status,
            registration_date=user_entity.registration_date if user_entity.registration_date else None, # Adicionado o mapeamento da data de registro
            address=address_response_data
        )