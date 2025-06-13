import pytest
from unittest.mock import Mock
import uuid
from tests.unit.mocks.factories import MockFactory

# Recursos compartilhados por todos os testes de usuário
mock_factory = MockFactory()

class BaseUserTest:
    """Classe base para todos os testes relacionados a usuários"""
    
    @pytest.fixture
    def test_ids(self):
        """Gera IDs consistentes para uso nos testes."""
        return {
            'user_id': str(uuid.uuid4()),
            'address_id': str(uuid.uuid4())
        }
    
    # Métodos e fixtures genéricos para todos os testes de usuário