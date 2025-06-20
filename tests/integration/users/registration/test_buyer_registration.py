import pytest
import json
import uuid
from tests.integration.conftest import mock_factory
import uuid

class TestBuyerRegistrationIntegration:
    """
    Testes de integração para o registro de compradores.
    Estes testes verificam se o endpoint de registro funciona corretamente,
    persistindo dados no banco e aplicando as regras de negócio.
    """

    @pytest.fixture
    def valid_buyer_data(self):
        """Dados válidos para registro de comprador usando o mock_factory."""
        # Cria objetos mock
        mock_buyer = mock_factory.buyer.create()
        mock_address = mock_factory.address.create()
        
        # Gera um email único
        unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
        
        # Retorna um dicionário para JSON
        return {
            "email": unique_email,
            "password": "ValidPassword123!",
            "full_name": mock_buyer.full_name,
            "phone": mock_buyer.phone,
            "address": {
                "street": mock_address.street,
                "number": mock_address.number,
                "complement": mock_address.complement,
                "neighborhood": mock_address.neighborhood,
                "city": mock_address.city,
                "state": mock_address.state,
                "zip_code": mock_address.zip_code,
                "country": mock_address.country
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
            error_found = False
        
            # Procura o erro em diferentes locais e formatos possíveis
            if "Invalid email format" in str(data):
                error_found = True  # Mensagem do serviço
            elif "email" in str(data.get('errors', '')):
                error_found = True  # Erro de campo específico
            elif "value_error.email" in str(data):
                error_found = True  # Erro de validação do Pydantic
            elif any("email" in str(detail).lower() for detail in data.get('details', [])):
                error_found = True  # Detalhes do erro (Flask-RESTx)
            elif "value is not a valid email" in str(data):
                error_found = True  # Mensagem de erro do Pydantic
            elif 'Input payload validation failed' in str(data):
                error_found = True  # Mensagem padrão do Pydantic v2
            elif "value_error" in str(data) and "email" in str(data):
                error_found = True  # Combinação de termos
                
            assert error_found, f"Mensagem de erro para {invalid_email} não contém referência ao email. Resposta: {data}"
            
            # Verifica que nenhum usuário foi criado com este email
            from app.infrastructure.persistence.models_db.user_db_model import UserDBModel
            user = UserDBModel.query.filter_by(email=invalid_email).first()
            assert user is None, f"Um usuário foi criado com email inválido: {invalid_email}"