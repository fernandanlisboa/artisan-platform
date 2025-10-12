import pytest
import jwt
import time
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock
from app.common.jwt_utils import JWTManager
from app.common.config import config_by_name


class TestJWTManager:
    """Unit tests for JWTManager class."""
    
    @pytest.fixture
    def test_config(self):
        """JWT test configuration."""
        return config_by_name['testing']
    
    @pytest.fixture
    def sample_user_data(self):
        """Sample user data for tests."""
        return {
            'user_id': 'test-user-123',
            'email': 'test@example.com'
        }
    
    def test_generate_access_token_success(self, test_config, sample_user_data):
        """Tests successful access token generation."""
        # Arrange
        user_id = sample_user_data['user_id']
        email = sample_user_data['email']
        
        # Act
        token = JWTManager.generate_access_token(user_id, email)
        
        # Assert
        assert token is not None
        assert isinstance(token, str)
        
        # Decode to verify content
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
        assert 'jti' in decoded  # Check JWT ID presence
    
    def test_generate_access_token_with_extra_claims(self, test_config, sample_user_data):
        """Tests access token generation with extra claims."""
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
        """Tests successful refresh token generation."""
        # Arrange
        user_id = sample_user_data['user_id']
        email = sample_user_data['email']
        
        # Act
        token = JWTManager.generate_refresh_token(user_id, email)
        
        # Assert
        assert token is not None
        assert isinstance(token, str)
        
        # Decode to verify content
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
        assert 'jti' in decoded  # Check JWT ID presence
    
    def test_decode_token_success(self, test_config, sample_user_data):
        """Tests successful token decoding."""
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
        """Tests decoding expired token."""
        # Arrange - Create token with past expiration
        user_id = sample_user_data['user_id']
        email = sample_user_data['email']
        
        now = datetime.now(timezone.utc)
        expired_time = now - timedelta(minutes=1)  # 1 minute ago
        
        payload = {
            'user_id': user_id,
            'email': email,
            'type': 'access',
            'iat': now.timestamp(),
            'exp': expired_time.timestamp(),  # Expired
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
        """Tests decoding token with invalid signature."""
        # Arrange - Create token with different secret key
        payload = {
            'user_id': 'test-user',
            'email': 'test@example.com',
            'type': 'access',
            'exp': (datetime.now(timezone.utc) + timedelta(minutes=30)).timestamp()
        }
        
        invalid_token = jwt.encode(
            payload,
            'wrong-secret-key',  # Wrong secret key
            algorithm=test_config.JWT_ALGORITHM
        )
        
        # Act & Assert
        with pytest.raises(jwt.InvalidTokenError):
            JWTManager.decode_token(invalid_token)
    
    def test_decode_token_malformed(self):
        """Tests decoding malformed token."""
        # Arrange
        malformed_token = "this.is.not.a.valid.jwt.token"
        
        # Act & Assert
        with pytest.raises(jwt.InvalidTokenError):
            JWTManager.decode_token(malformed_token)
    
    def test_verify_token_valid(self, test_config, sample_user_data):
        """Tests verification of valid token."""
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
        """Tests that verify_token returns None for expired token."""
        # Arrange - Create expired token
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
        """Tests that verify_token returns None for invalid token."""
        # Arrange
        invalid_token = "invalid.jwt.token"
        
        # Act
        result = JWTManager.verify_token(invalid_token)
        
        # Assert
        assert result is None
    
    def test_token_expiration_time_access_simple(self, test_config, sample_user_data):
        """Tests if access token expiration time is within expected range."""
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
        """Tests if refresh token expiration time is within expected range."""
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
        """Tests if 'type' field is correct in access token."""
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
        """Tests if 'type' field is correct in refresh token."""
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
        """Tests if token has all required fields."""
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
            assert field in access_decoded, f"Field '{field}' missing in access token"
        
        # Assert - Refresh Token
        refresh_decoded = jwt.decode(
            refresh_token, 
            test_config.JWT_SECRET_KEY, 
            algorithms=[test_config.JWT_ALGORITHM]
        )
        
        for field in required_fields:
            assert field in refresh_decoded, f"Field '{field}' missing in refresh token"
    
    def test_tokens_are_different_for_same_user(self, sample_user_data):
        """Tests if tokens generated at different times are unique."""
        # Arrange
        user_id = sample_user_data['user_id']
        email = sample_user_data['email']
        
        # Act
        token1 = JWTManager.generate_access_token(user_id, email)
        # Small pause to ensure different timestamps
        time.sleep(0.001)  # 1ms pause
        token2 = JWTManager.generate_access_token(user_id, email)
        
        # Assert
        assert token1 != token2, "Tokens must be unique even for same user"
        
        # Verify that JTIs are different
        decoded1 = JWTManager.decode_token(token1)
        decoded2 = JWTManager.decode_token(token2)
        assert decoded1['jti'] != decoded2['jti'], "JWT IDs must be unique"
    
    def test_decode_token_validates_exp_by_default(self, test_config, sample_user_data):
        """Tests if decoding validates expiration by default."""
        # Arrange - Valid token
        user_id = sample_user_data['user_id']
        email = sample_user_data['email']
        valid_token = JWTManager.generate_access_token(user_id, email)
        
        # Act & Assert - Valid token should work
        decoded = JWTManager.decode_token(valid_token)
        assert decoded['user_id'] == user_id
        
        # Arrange - Expired token
        now = datetime.now(timezone.utc)
        expired_payload = {
            'user_id': user_id,
            'email': email,
            'type': 'access',
            'iat': now.timestamp(),
            'exp': (now - timedelta(seconds=1)).timestamp(),  # Expired 1 second ago
            'nbf': now.timestamp()
        }
        
        expired_token = jwt.encode(
            expired_payload,
            test_config.JWT_SECRET_KEY,
            algorithm=test_config.JWT_ALGORITHM
        )
        
        # Act & Assert - Expired token should fail
        with pytest.raises(jwt.ExpiredSignatureError):
            JWTManager.decode_token(expired_token)
    
    def test_jti_uniqueness(self, sample_user_data):
        """Tests if JWT IDs are unique."""
        # Arrange
        user_id = sample_user_data['user_id']
        email = sample_user_data['email']
        
        # Act - Generate multiple tokens
        tokens = []
        jtis = []
        
        for _ in range(5):
            token = JWTManager.generate_access_token(user_id, email)
            decoded = JWTManager.decode_token(token)
            tokens.append(token)
            jtis.append(decoded['jti'])
        
        # Assert - All tokens must be different
        assert len(set(tokens)) == 5, "All tokens must be unique"
        
        # Assert - All JTIs must be different
        assert len(set(jtis)) == 5, "All JWT IDs must be unique"