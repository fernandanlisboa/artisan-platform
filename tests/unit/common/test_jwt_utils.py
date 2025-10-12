import pytest
import jwt
import time
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock
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
        assert 'jti' in decoded  # Verificar presença do JWT ID
    
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
        assert 'jti' in decoded  # Verificar presença do JWT ID
    
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
            'iat': now.timestamp(),
            'exp': expired_time.timestamp(),  # Expirado
            'nbf': now.timestamp()
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
            'exp': (datetime.now(timezone.utc) + timedelta(minutes=30)).timestamp()
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
            'iat': now.timestamp(),
            'exp': expired_time.timestamp(),
            'nbf': now.timestamp()
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
    
    def test_token_expiration_time_access_simple(self, test_config, sample_user_data):
        """Testa se o tempo de expiração do token de acesso está dentro do range esperado."""
        # Arrange
        user_id = sample_user_data['user_id']
        email = sample_user_data['email']
        before_generation = datetime.now(timezone.utc)
        
        # Act
        token = JWTManager.generate_access_token(user_id, email)
        after_generation = datetime.now(timezone.utc)
        
        # Assert
        decoded = jwt.decode(
            token, 
            test_config.JWT_SECRET_KEY, 
            algorithms=[test_config.JWT_ALGORITHM],
            options={"verify_exp": False}
        )
        
        actual_exp = datetime.fromtimestamp(decoded['exp'], tz=timezone.utc)
        expected_min = before_generation + timedelta(minutes=test_config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        expected_max = after_generation + timedelta(minutes=test_config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        
        assert expected_min <= actual_exp <= expected_max
    
    def test_token_expiration_time_refresh_simple(self, test_config, sample_user_data):
        """Testa se o tempo de expiração do token de refresh está dentro do range esperado."""
        # Arrange
        user_id = sample_user_data['user_id']
        email = sample_user_data['email']
        before_generation = datetime.now(timezone.utc)
        
        # Act
        token = JWTManager.generate_refresh_token(user_id, email)
        after_generation = datetime.now(timezone.utc)
        
        # Assert
        decoded = jwt.decode(
            token, 
            test_config.JWT_SECRET_KEY, 
            algorithms=[test_config.JWT_ALGORITHM],
            options={"verify_exp": False}
        )
        
        actual_exp = datetime.fromtimestamp(decoded['exp'], tz=timezone.utc)
        expected_min = before_generation + timedelta(days=test_config.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
        expected_max = after_generation + timedelta(days=test_config.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
        
        assert expected_min <= actual_exp <= expected_max
    
    def test_access_token_type_field(self, test_config, sample_user_data):
        """Testa se o campo 'type' está correto no token de acesso."""
        # Arrange
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
        
        assert decoded['type'] == 'access'
    
    def test_refresh_token_type_field(self, test_config, sample_user_data):
        """Testa se o campo 'type' está correto no token de refresh."""
        # Arrange
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
        
        assert decoded['type'] == 'refresh'
    
    def test_token_has_required_fields(self, test_config, sample_user_data):
        """Testa se o token possui todos os campos obrigatórios."""
        # Arrange
        user_id = sample_user_data['user_id']
        email = sample_user_data['email']
        
        # Act
        access_token = JWTManager.generate_access_token(user_id, email)
        refresh_token = JWTManager.generate_refresh_token(user_id, email)
        
        # Assert - Access Token
        access_decoded = jwt.decode(
            access_token, 
            test_config.JWT_SECRET_KEY, 
            algorithms=[test_config.JWT_ALGORITHM]
        )
        
        required_fields = ['user_id', 'email', 'type', 'iat', 'exp', 'nbf', 'jti']
        for field in required_fields:
            assert field in access_decoded, f"Campo '{field}' ausente no access token"
        
        # Assert - Refresh Token
        refresh_decoded = jwt.decode(
            refresh_token, 
            test_config.JWT_SECRET_KEY, 
            algorithms=[test_config.JWT_ALGORITHM]
        )
        
        for field in required_fields:
            assert field in refresh_decoded, f"Campo '{field}' ausente no refresh token"
    
    def test_tokens_are_different_for_same_user(self, sample_user_data):
        """Testa se tokens gerados em momentos diferentes são únicos."""
        # Arrange
        user_id = sample_user_data['user_id']
        email = sample_user_data['email']
        
        # Act
        token1 = JWTManager.generate_access_token(user_id, email)
        # Pequena pausa para garantir timestamps diferentes
        time.sleep(0.001)  # 1ms de pausa
        token2 = JWTManager.generate_access_token(user_id, email)
        
        # Assert
        assert token1 != token2, "Tokens devem ser únicos mesmo para o mesmo usuário"
        
        # Verificar que os JTI são diferentes
        decoded1 = JWTManager.decode_token(token1)
        decoded2 = JWTManager.decode_token(token2)
        assert decoded1['jti'] != decoded2['jti'], "JWT IDs devem ser únicos"
    
    def test_decode_token_validates_exp_by_default(self, test_config, sample_user_data):
        """Testa se por padrão a decodificação valida a expiração."""
        # Arrange - Token válido
        user_id = sample_user_data['user_id']
        email = sample_user_data['email']
        valid_token = JWTManager.generate_access_token(user_id, email)
        
        # Act & Assert - Token válido deve funcionar
        decoded = JWTManager.decode_token(valid_token)
        assert decoded['user_id'] == user_id
        
        # Arrange - Token expirado
        now = datetime.now(timezone.utc)
        expired_payload = {
            'user_id': user_id,
            'email': email,
            'type': 'access',
            'iat': now.timestamp(),
            'exp': (now - timedelta(seconds=1)).timestamp(),  # Expirado há 1 segundo
            'nbf': now.timestamp()
        }
        
        expired_token = jwt.encode(
            expired_payload,
            test_config.JWT_SECRET_KEY,
            algorithm=test_config.JWT_ALGORITHM
        )
        
        # Act & Assert - Token expirado deve falhar
        with pytest.raises(jwt.ExpiredSignatureError):
            JWTManager.decode_token(expired_token)
    
    def test_jti_uniqueness(self, sample_user_data):
        """Testa se os JWT IDs são únicos."""
        # Arrange
        user_id = sample_user_data['user_id']
        email = sample_user_data['email']
        
        # Act - Gerar múltiplos tokens
        tokens = []
        jtis = []
        
        for _ in range(5):
            token = JWTManager.generate_access_token(user_id, email)
            decoded = JWTManager.decode_token(token)
            tokens.append(token)
            jtis.append(decoded['jti'])
        
        # Assert - Todos os tokens devem ser diferentes
        assert len(set(tokens)) == 5, "Todos os tokens devem ser únicos"
        
        # Assert - Todos os JTIs devem ser diferentes
        assert len(set(jtis)) == 5, "Todos os JWT IDs devem ser únicos"