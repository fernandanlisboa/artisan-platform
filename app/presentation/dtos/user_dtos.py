from pydantic import BaseModel, Field
from typing import Optional
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
