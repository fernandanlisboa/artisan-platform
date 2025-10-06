import pytest
import jwt
from datetime import datetime, timedelta, timezone
from unittest.mock import patch
from app.common.jwt_utils import JWTManager
from app.common.config import config_by_name


class TestJWTManager:
    """Testes unitários para a classe JWTManager."""
    
    @pytest.fixture
    def test_config(self):
        """Configuração de teste para JWT."""
        return config_by_name['testing']
    
    @pytest.fixture
    def sample_user_data(self):
        """Dados de usuário de exemplo para os testes."""
        return {
            'user_id': 'test-user-123',
            'email': 'test@example.com'
        }
    
    def test_generate_access_token_success(self, test_config, sample_user_data):
        """Testa a geração bem-sucedida de token de acesso."""
        # Arrange
        user_id = sample_user_data['user_id']
        email = sample_user_data['email']
        
        # Act
        token = JWTManager.generate_access_token(user_id, email)
        
        # Assert
        assert token is not None
        assert isinstance(token, str)
        
        # Decode para verificar o conteúdo
        decoded = jwt.decode(
            token, 
            test_config.JWT_SECRET_KEY, 
            algorithms=[test_config.JWT_ALGORITHM]
        )
        
        assert decoded['user_id'] == user_id
        assert decoded['email'] == email
        assert decoded['type'] == 'access'
        assert 'iat' in decoded
        assert 'exp' in decoded
        assert 'nbf' in decoded
    
    def test_generate_access_token_with_extra_claims(self, test_config, sample_user_data):
        """Testa a geração de token de acesso com claims extras."""
        # Arrange
        user_id = sample_user_data['user_id']
        email = sample_user_data['email']
        extra_claims = {'role': 'artisan', 'permissions': ['create_product']}
        
        # Act
        token = JWTManager.generate_access_token(user_id, email, **extra_claims)
        
        # Assert
        decoded = jwt.decode(
            token, 
            test_config.JWT_SECRET_KEY, 
            algorithms=[test_config.JWT_ALGORITHM]
        )
        
        assert decoded['role'] == 'artisan'
        assert decoded['permissions'] == ['create_product']
    
    def test_generate_refresh_token_success(self, test_config, sample_user_data):
        """Testa a geração bem-sucedida de token de refresh."""
        # Arrange
        user_id = sample_user_data['user_id']
        email = sample_user_data['email']
        
        # Act
        token = JWTManager.generate_refresh_token(user_id, email)
        
        # Assert
        assert token is not None
        assert isinstance(token, str)
        
        # Decode para verificar o conteúdo
        decoded = jwt.decode(
            token, 
            test_config.JWT_SECRET_KEY, 
            algorithms=[test_config.JWT_ALGORITHM]
        )
        
        assert decoded['user_id'] == user_id
        assert decoded['email'] == email
        assert decoded['type'] == 'refresh'
        assert 'iat' in decoded
        assert 'exp' in decoded
        assert 'nbf' in decoded
    
    def test_decode_token_success(self, test_config, sample_user_data):
        """Testa a decodificação bem-sucedida de token."""
        # Arrange
        user_id = sample_user_data['user_id']
        email = sample_user_data['email']
        token = JWTManager.generate_access_token(user_id, email)
        
        # Act
        decoded = JWTManager.decode_token(token)
        
        # Assert
        assert decoded['user_id'] == user_id
        assert decoded['email'] == email
        assert decoded['type'] == 'access'
    
    def test_decode_token_expired(self, test_config, sample_user_data):
        """Testa a decodificação de token expirado."""
        # Arrange - Cria um token com expiração no passado
        user_id = sample_user_data['user_id']
        email = sample_user_data['email']
        
        now = datetime.now(timezone.utc)
        expired_time = now - timedelta(minutes=1)  # 1 minuto atrás
        
        payload = {
            'user_id': user_id,
            'email': email,
            'type': 'access',
            'iat': now,
            'exp': expired_time,  # Expirado
            'nbf': now
        }
        
        expired_token = jwt.encode(
            payload,
            test_config.JWT_SECRET_KEY,
            algorithm=test_config.JWT_ALGORITHM
        )
        
        # Act & Assert
        with pytest.raises(jwt.ExpiredSignatureError):
            JWTManager.decode_token(expired_token)
    
    def test_decode_token_invalid_signature(self, test_config):
        """Testa a decodificação de token com assinatura inválida."""
        # Arrange - Cria um token com chave secreta diferente
        payload = {
            'user_id': 'test-user',
            'email': 'test@example.com',
            'type': 'access',
            'exp': datetime.now(timezone.utc) + timedelta(minutes=30)
        }
        
        invalid_token = jwt.encode(
            payload,
            'wrong-secret-key',  # Chave secreta incorreta
            algorithm=test_config.JWT_ALGORITHM
        )
        
        # Act & Assert
        with pytest.raises(jwt.InvalidTokenError):
            JWTManager.decode_token(invalid_token)
    
    def test_decode_token_malformed(self):
        """Testa a decodificação de token mal formado."""
        # Arrange
        malformed_token = "this.is.not.a.valid.jwt.token"
        
        # Act & Assert
        with pytest.raises(jwt.InvalidTokenError):
            JWTManager.decode_token(malformed_token)
    
    def test_verify_token_valid(self, test_config, sample_user_data):
        """Testa a verificação de token válido."""
        # Arrange
        user_id = sample_user_data['user_id']
        email = sample_user_data['email']
        token = JWTManager.generate_access_token(user_id, email)
        
        # Act
        result = JWTManager.verify_token(token)
        
        # Assert
        assert result is not None
        assert result['user_id'] == user_id
        assert result['email'] == email
    
    def test_verify_token_expired_returns_none(self, test_config, sample_user_data):
        """Testa que verify_token retorna None para token expirado."""
        # Arrange - Cria um token expirado
        user_id = sample_user_data['user_id']
        email = sample_user_data['email']
        
        now = datetime.now(timezone.utc)
        expired_time = now - timedelta(minutes=1)
        
        payload = {
            'user_id': user_id,
            'email': email,
            'type': 'access',
            'iat': now,
            'exp': expired_time,
            'nbf': now
        }
        
        expired_token = jwt.encode(
            payload,
            test_config.JWT_SECRET_KEY,
            algorithm=test_config.JWT_ALGORITHM
        )
        
        # Act
        result = JWTManager.verify_token(expired_token)
        
        # Assert
        assert result is None
    
    def test_verify_token_invalid_returns_none(self):
        """Testa que verify_token retorna None para token inválido."""
        # Arrange
        invalid_token = "invalid.jwt.token"
        
        # Act
        result = JWTManager.verify_token(invalid_token)
        
        # Assert
        assert result is None
    
    @patch('app.common.jwt_utils.datetime')
    def test_token_expiration_time_access(self, mock_datetime, test_config, sample_user_data):
        """Testa se o tempo de expiração do token de acesso está correto."""
        # Arrange
        fixed_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_datetime.now.return_value = fixed_time
        
        user_id = sample_user_data['user_id']
        email = sample_user_data['email']
        
        # Act
        token = JWTManager.generate_access_token(user_id, email)
        
        # Assert
        decoded = jwt.decode(
            token, 
            test_config.JWT_SECRET_KEY, 
            algorithms=[test_config.JWT_ALGORITHM]
        )
        
        expected_exp = fixed_time + timedelta(minutes=test_config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        actual_exp = datetime.fromtimestamp(decoded['exp'], tz=timezone.utc)
        
        assert actual_exp == expected_exp
    
    @patch('app.common.jwt_utils.datetime')
    def test_token_expiration_time_refresh(self, mock_datetime, test_config, sample_user_data):
        """Testa se o tempo de expiração do token de refresh está correto."""
        # Arrange
        fixed_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_datetime.now.return_value = fixed_time
        
        user_id = sample_user_data['user_id']
        email = sample_user_data['email']
        
        # Act
        token = JWTManager.generate_refresh_token(user_id, email)
        
        # Assert
        decoded = jwt.decode(
            token, 
            test_config.JWT_SECRET_KEY, 
            algorithms=[test_config.JWT_ALGORITHM]
        )
        
        expected_exp = fixed_time + timedelta(days=test_config.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
        actual_exp = datetime.fromtimestamp(decoded['exp'], tz=timezone.utc)
        
        assert actual_exp == expected_exp