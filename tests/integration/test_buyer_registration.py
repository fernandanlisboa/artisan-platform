import pytest
import json
import uuid
from app import db

class TestBuyerRegistrationIntegration:
    """
    Testes de integração para o registro de compradores.
    Estes testes verificam se o endpoint de registro funciona corretamente,
    persistindo dados no banco e aplicando as regras de negócio.
    """

    @pytest.fixture
    def valid_buyer_data(self):
        """Dados válidos para registro de comprador."""
        # Sempre use email único para evitar conflitos entre testes
        unique_email = f"buyer.{uuid.uuid4().hex[:8]}@example.com"
        return {
            "email": unique_email,
            "password": "Secure123Password!",
            "full_name": "Comprador Teste",
            "phone": "(71) 99876-5432",
            "address": {
                "street": "Avenida dos Compradores",
                "number": "456",
                "complement": "Casa 2",
                "neighborhood": "Centro",
                "city": "Salvador",
                "state": "BA",
                "zip_code": "41000-000",
                "country": "Brasil"
            }
        }

    def test_buyer_registration_success(self, client, session, valid_buyer_data):
        """
        Teste principal: Verifica se o registro de comprador funciona com dados válidos.
        Este é o primeiro teste a ser escrito em TDD.
        """
        # Act
        response = client.post(
            '/api/auth/register/buyer',
            json=valid_buyer_data,
            content_type='application/json'
        )
        
        # Assert - Status code
        assert response.status_code == 201
        
        # Assert - Response body
        data = json.loads(response.data)
        assert 'user_id' in data
        assert data['email'] == valid_buyer_data['email']
        assert data['full_name'] == valid_buyer_data['full_name']
        assert data['phone'] == valid_buyer_data['phone']
        assert data['status'] == 'active'
        assert data['role'] == 'buyer'
        
        # Assert - Database state
        from app.infrastructure.persistence.models_db.user_db_model import UserDBModel
        from app.infrastructure.persistence.models_db.buyer_db_model import BuyerDBModel
        
        # Verifica se o usuário foi persistido
        user = UserDBModel.query.filter_by(email=valid_buyer_data['email']).first()
        assert user is not None
        
        # Verifica se o comprador foi persistido
        buyer = BuyerDBModel.query.filter_by(buyer_id=user.user_id).first()
        assert buyer is not None
        assert buyer.full_name == valid_buyer_data['full_name']

    def test_duplicate_email_registration(self, client, session, valid_buyer_data):
        """Verifica se a API impede registro com email duplicado."""
        # Arrange - Primeiro registro
        response = client.post(
            '/api/auth/register/buyer',
            json=valid_buyer_data,
            content_type='application/json'
        )
        assert response.status_code == 201
        
        # Act - Tenta registrar com o mesmo email
        response = client.post(
            '/api/auth/register/buyer',
            json=valid_buyer_data,
            content_type='application/json'
        )
        
        # Assert
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "Email already registered" in data.get('message', '')

    def test_weak_password_validation(self, client, session, valid_buyer_data):
        """Verifica se a API valida senhas fracas."""
        # Arrange
        valid_buyer_data['password'] = "weak"
        
        # Act
        response = client.post(
            '/api/auth/register/buyer',
            json=valid_buyer_data,
            content_type='application/json'
        )
        
        # Assert
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "password" in data.get('errors', '')

    def test_address_reuse(self, client, session, valid_buyer_data):
        """
        Verifica se endereços idênticos são reutilizados ao invés de duplicados.
        Isso testa uma regra de negócio importante para manter a integridade dos dados.
        """
        response = client.post(
            '/api/auth/register/buyer',
            json=valid_buyer_data,
            content_type='application/json'
        )
        data1 = json.loads(response.data)
        # Assert
        assert response.status_code == 201, "Registro do primeiro comprador falhou!"
        
        
        # Modifica o email para criar outro comprador com o mesmo endereço
        valid_buyer_data['email'] = f"another.buyer.{uuid.uuid4().hex[:8]}@example.com"
        
        # Act - Segundo registro com mesmo endereço
        response = client.post(
            '/api/auth/register/buyer',
            json=valid_buyer_data,
            content_type='application/json'
        )
        data2 = json.loads(response.data)
        
        # Assert
        assert response.status_code == 201
        
        # Verifica se o segundo usuário foi criado com o mesmo address_id
        assert data2 is not None, "usário com mesmo endereço não criado!"
        assert data1["address"]["address_id"] == data2["address"]["address_id"], "O endereço não foi reutilizado"
        
        # Verifica quantos registros de endereço existem com esses dados
        from app.infrastructure.persistence.models_db.address_db_model import AddressDBModel
        address_count = AddressDBModel.query.filter_by(
            street=valid_buyer_data['address']['street'],
            number=valid_buyer_data['address']['number']
        ).count()
        assert address_count == 1, "Endereço foi duplicado indevidamente"

    def test_missing_required_fields(self, client, session, valid_buyer_data):
        """Verifica se a API valida campos obrigatórios ausentes."""
        # Arrange - Remove campos obrigatórios
        del valid_buyer_data['email']
        
        # Act
        response = client.post(
            '/api/auth/register/buyer',
            json=valid_buyer_data,
            content_type='application/json'
        )
        
        # Assert
        assert response.status_code == 400

    def test_invalid_email_format(self, client, session, valid_buyer_data):
        """Verifica se a API rejeita emails com formato inválido."""
        # Arrange - Teste com diversos formatos inválidos
        invalid_emails = [
            "plainaddress",       # Sem @ e domínio
            "@missinglocal.org",  # Sem parte local
            "user@.com",          # Domínio inválido
            "user@domain",        # Sem TLD
            "a" * 65 + "@example.com"  # Parte local muito longa
        ]
        
        for invalid_email in invalid_emails:
            # Modifica o email para um formato inválido
            valid_buyer_data['email'] = invalid_email
            if invalid_email == "a" * 65 + "@example.com":
                print("x")
            # Act - Faz a requisição para a API
            response = client.post(
                '/api/auth/register/buyer',
                json=valid_buyer_data,
                content_type='application/json'
            )
            
            # Assert - Verifica se foi rejeitado corretamente
            assert response.status_code == 400, f"Email {invalid_email} deveria ser rejeitado"
            data = json.loads(response.data)
            assert "Invalid email format" in data.get('message', '') or \
                   "email" in data.get('errors', ''), \
                   f"Mensagem de erro para {invalid_email} não contém referência ao email"
            
            # Verifica que nenhum usuário foi criado com este email
            from app.infrastructure.persistence.models_db.user_db_model import UserDBModel
            user = UserDBModel.query.filter_by(email=invalid_email).first()
            assert user is None, f"Um usuário foi criado com email inválido: {invalid_email}"