# Em tests/unit/test_dtos.py
import pytest
from pydantic import ValidationError
from app.presentation.dtos.user_dtos import RegisterBuyerRequest, RegisterAddressRequest

class TestUserDTOs:
    
    @pytest.fixture
    def valid_address_data(self):
        """Endereço válido para testes."""
        return {
            "street": "Rua de Teste",
            "number": "123",
            "neighborhood": "Bairro Teste",
            "city": "Cidade Teste",
            "state": "BA",
            "zip_code": "40000-000",
            "country": "Brasil"
        }
    
    @pytest.mark.parametrize("invalid_email", [
        "",                   # Vazio
        "plainaddress",       # Sem @ e domínio
        "@missinglocal.org",  # Sem parte local
        "user@.com",          # Domínio inválido
        "user@domain",        # Sem TLD
        "user@domain..com",   # Ponto duplo
        None,                 # Nulo
        "a" * 65 + "@example.com"  # Parte local muito longa
    ])
    def test_buyer_request_invalid_email(self, invalid_email, valid_address_data):
        """Testa validação de email diretamente no DTO usando Pydantic."""
    
        # Dados válidos para os outros campos obrigatórios
        valid_data = {
            "password": "ValidPassword123!",
            "full_name": "Nome Teste",
            "address": {
                "street": "Rua Teste",
                "number": "123",
                "neighborhood": "Bairro Teste",
                "city": "Cidade Teste",
                "state": "BA",
                "zip_code": "40000-000",
                "country": "Brasil"
            }
        }
        # Adiciona o email inválido aos dados
        test_data = {**valid_data, "email": invalid_email}
        
        # Verifica se a validação do Pydantic rejeita o email
        with pytest.raises(ValidationError) as exc_info:
            RegisterBuyerRequest(**test_data)
