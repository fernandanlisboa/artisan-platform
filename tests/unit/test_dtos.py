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
        """Testa validação de diferentes formatos inválidos de email no DTO."""
        
        # Dados do comprador com email inválido
        data = {
            "email": invalid_email,
            "password": "ValidPassword123!",
            "full_name": "Comprador Teste",
            "phone": "(71) 98765-4321",
            "address": valid_address_data  # Passar o dicionário diretamente, não um objeto instanciado
        }
        
        # Act & Assert - Deve lançar ValidationError
        with pytest.raises(ValidationError) as excinfo:
            buyer_request = RegisterBuyerRequest(**data)
        
        # Verifica se o erro está relacionado ao campo email
        errors = excinfo.value.errors()
        assert any(error["loc"][0] == "email" for error in errors)