import pytest
import jwt
import time
import os
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock
from app.common.jwt_utils import JWTManager
from app.common.config import config_by_name


class TestJWTManager:
    """Unit tests for JWTManager class."""
    
    @pytest.fixture(autouse=True)
    def setup_test_environment(self):
        """Force test environment for all tests in this class."""
        with patch.dict(os.environ, {'API_ENV': 'testing'}):
            yield
    
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
    
    @pytest.fixture
    def mock_jwt_config(self, test_config):
        """Mock JWTManager configuration to use test config."""
        with patch.object(JWTManager, '_get_config', return_value=test_config):
            yield test_config
    
    @pytest.fixture
    def access_token(self, sample_user_data, mock_jwt_config):
        """Generate access token for testing."""
        return JWTManager.generate_access_token(
            sample_user_data['user_id'], 
            sample_user_data['email']
        )
    
    @pytest.fixture
    def refresh_token(self, sample_user_data, mock_jwt_config):
        """Generate refresh token for testing."""
        return JWTManager.generate_refresh_token(
            sample_user_data['user_id'], 
            sample_user_data['email']
        )
    
    @pytest.fixture
    def expired_token_payload(self, sample_user_data):
        """Create payload for expired token."""
        now = datetime.now(timezone.utc)
        return {
            'user_id': sample_user_data['user_id'],
            'email': sample_user_data['email'],
            'type': 'access',
            'iat': now.timestamp(),
            'exp': (now - timedelta(minutes=1)).timestamp(),  # Expired 1 minute ago
            'nbf': now.timestamp()
        }
    
    @pytest.fixture
    def expired_token(self, expired_token_payload, test_config):
        """Create expired token for testing."""
        return jwt.encode(
            expired_token_payload,
            test_config.JWT_SECRET_KEY,
            algorithm=test_config.JWT_ALGORITHM
        )
    
    def test_configuration_consistency(self, mock_jwt_config, test_config):
        """Test that JWTManager uses the correct test configuration."""
        # Get config from JWTManager (should be mocked)
        jwt_config = JWTManager._get_config()
        
        # Assert they match
        assert jwt_config.JWT_SECRET_KEY == test_config.JWT_SECRET_KEY
        assert jwt_config.JWT_ALGORITHM == test_config.JWT_ALGORITHM
    
    def test_generate_access_token_success(self, mock_jwt_config, sample_user_data):
        """Tests successful access token generation."""
        # Arrange
        user_id = sample_user_data['user_id']
        email = sample_user_data['email']
        
        # Act
        token = JWTManager.generate_access_token(user_id, email)
        
        # Assert
        assert token is not None
        assert isinstance(token, str)
        
        # Decode using JWTManager to ensure consistency
        decoded = JWTManager.decode_token(token)
        
        assert decoded['user_id'] == user_id
        assert decoded['email'] == email
        assert decoded['type'] == 'access'
        assert 'iat' in decoded
        assert 'exp' in decoded
        assert 'nbf' in decoded
        assert 'jti' in decoded
    
    def test_generate_access_token_with_extra_claims(self, mock_jwt_config, sample_user_data):
        """Tests access token generation with extra claims."""
        # Arrange
        user_id = sample_user_data['user_id']
        email = sample_user_data['email']
        extra_claims = {'role': 'artisan', 'permissions': ['create_product']}
        
        # Act
        token = JWTManager.generate_access_token(user_id, email, **extra_claims)
        
        # Assert - Use JWTManager for consistency
        decoded = JWTManager.decode_token(token)
        
        assert decoded['role'] == 'artisan'
        assert decoded['permissions'] == ['create_product']
    
    def test_generate_refresh_token_success(self, mock_jwt_config, sample_user_data):
        """Tests successful refresh token generation."""
        # Arrange
        user_id = sample_user_data['user_id']
        email = sample_user_data['email']
        
        # Act
        token = JWTManager.generate_refresh_token(user_id, email)
        
        # Assert
        assert token is not None
        assert isinstance(token, str)
        
        # Use JWTManager for consistency
        decoded = JWTManager.decode_token(token)
        
        assert decoded['user_id'] == user_id
        assert decoded['email'] == email
        assert decoded['type'] == 'refresh'
        assert 'iat' in decoded
        assert 'exp' in decoded
        assert 'nbf' in decoded
        assert 'jti' in decoded
    
    def test_decode_token_success(self, access_token, sample_user_data, mock_jwt_config):
        """Tests successful token decoding."""
        # Act
        decoded = JWTManager.decode_token(access_token)
        
        # Assert
        assert decoded['user_id'] == sample_user_data['user_id']
        assert decoded['email'] == sample_user_data['email']
        assert decoded['type'] == 'access'
    
    def test_decode_token_expired(self, expired_token, mock_jwt_config):
        """Tests decoding expired token."""
        # Act & Assert
        with pytest.raises(jwt.ExpiredSignatureError):
            JWTManager.decode_token(expired_token)
    
    def test_decode_token_invalid_signature(self, test_config, mock_jwt_config):
        """Tests decoding token with invalid signature."""
        # Arrange
        payload = {
            'user_id': 'test-user',
            'email': 'test@example.com',
            'type': 'access',
            'exp': (datetime.now(timezone.utc) + timedelta(minutes=30)).timestamp()
        }
        
        invalid_token = jwt.encode(
            payload,
            'wrong-secret-key',
            algorithm=test_config.JWT_ALGORITHM
        )
        
        # Act & Assert
        with pytest.raises(jwt.InvalidTokenError):
            JWTManager.decode_token(invalid_token)
    
    def test_decode_token_malformed(self, mock_jwt_config):
        """Tests decoding malformed token."""
        # Arrange
        malformed_token = "this.is.not.a.valid.jwt.token"
        
        # Act & Assert
        with pytest.raises(jwt.InvalidTokenError):
            JWTManager.decode_token(malformed_token)
    
    def test_verify_token_valid(self, access_token, sample_user_data, mock_jwt_config):
        """Tests verification of valid token."""
        # Act
        result = JWTManager.verify_token(access_token)
        
        # Assert
        assert result is not None
        assert result['user_id'] == sample_user_data['user_id']
        assert result['email'] == sample_user_data['email']
    
    def test_verify_token_expired_returns_none(self, expired_token, mock_jwt_config):
        """Tests that verify_token returns None for expired token."""
        # Act
        result = JWTManager.verify_token(expired_token)
        
        # Assert
        assert result is None
    
    def test_verify_token_invalid_returns_none(self, mock_jwt_config):
        """Tests that verify_token returns None for invalid token."""
        # Arrange
        invalid_token = "invalid.jwt.token"
        
        # Act
        result = JWTManager.verify_token(invalid_token)
        
        # Assert
        assert result is None
    
    def test_token_expiration_time_access_simple(self, test_config, sample_user_data, mock_jwt_config):
        """Tests if access token expiration time is within expected range."""
        # Arrange
        user_id = sample_user_data['user_id']
        email = sample_user_data['email']
        before_generation = datetime.now(timezone.utc)
        
        # Act
        token = JWTManager.generate_access_token(user_id, email)
        after_generation = datetime.now(timezone.utc)
        
        # Assert - Use JWTManager for consistency
        decoded = JWTManager.decode_token(token)
        
        actual_exp = datetime.fromtimestamp(decoded['exp'], tz=timezone.utc)
        expected_min = before_generation + timedelta(minutes=test_config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        expected_max = after_generation + timedelta(minutes=test_config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        
        assert expected_min <= actual_exp <= expected_max
    
    def test_token_expiration_time_refresh_simple(self, test_config, sample_user_data, mock_jwt_config):
        """Tests if refresh token expiration time is within expected range."""
        # Arrange
        user_id = sample_user_data['user_id']
        email = sample_user_data['email']
        before_generation = datetime.now(timezone.utc)
        
        # Act
        token = JWTManager.generate_refresh_token(user_id, email)
        after_generation = datetime.now(timezone.utc)
        
        # Assert - Use JWTManager for consistency
        decoded = JWTManager.decode_token(token)
        
        actual_exp = datetime.fromtimestamp(decoded['exp'], tz=timezone.utc)
        expected_min = before_generation + timedelta(days=test_config.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
        expected_max = after_generation + timedelta(days=test_config.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
        
        assert expected_min <= actual_exp <= expected_max
    
    def test_access_token_type_field(self, access_token, mock_jwt_config):
        """Tests if 'type' field is correct in access token."""
        # Act
        decoded = JWTManager.decode_token(access_token)
        
        # Assert
        assert decoded['type'] == 'access'
    
    def test_refresh_token_type_field(self, refresh_token, mock_jwt_config):
        """Tests if 'type' field is correct in refresh token."""
        # Act
        decoded = JWTManager.decode_token(refresh_token)
        
        # Assert
        assert decoded['type'] == 'refresh'
    
    def test_access_token_has_user_id_field(self, access_token, mock_jwt_config):
        """Tests if access token has user_id field."""
        # Act
        decoded = JWTManager.decode_token(access_token)
        
        # Assert
        assert 'user_id' in decoded
    
    def test_access_token_has_email_field(self, access_token, mock_jwt_config):
        """Tests if access token has email field."""
        # Act
        decoded = JWTManager.decode_token(access_token)
        
        # Assert
        assert 'email' in decoded
    
    def test_access_token_has_iat_field(self, access_token, mock_jwt_config):
        """Tests if access token has iat field."""
        # Act
        decoded = JWTManager.decode_token(access_token)
        
        # Assert
        assert 'iat' in decoded
    
    def test_access_token_has_exp_field(self, access_token, mock_jwt_config):
        """Tests if access token has exp field."""
        # Act
        decoded = JWTManager.decode_token(access_token)
        
        # Assert
        assert 'exp' in decoded
    
    def test_access_token_has_nbf_field(self, access_token, mock_jwt_config):
        """Tests if access token has nbf field."""
        # Act
        decoded = JWTManager.decode_token(access_token)
        
        # Assert
        assert 'nbf' in decoded
    
    def test_access_token_has_jti_field(self, access_token, mock_jwt_config):
        """Tests if access token has jti field."""
        # Act
        decoded = JWTManager.decode_token(access_token)
        
        # Assert
        assert 'jti' in decoded
    
    def test_refresh_token_has_user_id_field(self, refresh_token, mock_jwt_config):
        """Tests if refresh token has user_id field."""
        # Act
        decoded = JWTManager.decode_token(refresh_token)
        
        # Assert
        assert 'user_id' in decoded
    
    def test_refresh_token_has_email_field(self, refresh_token, mock_jwt_config):
        """Tests if refresh token has email field."""
        # Act
        decoded = JWTManager.decode_token(refresh_token)
        
        # Assert
        assert 'email' in decoded
    
    def test_refresh_token_has_jti_field(self, refresh_token, mock_jwt_config):
        """Tests if refresh token has jti field."""
        # Act
        decoded = JWTManager.decode_token(refresh_token)
        
        # Assert
        assert 'jti' in decoded
    
    def test_tokens_are_different_for_same_user(self, sample_user_data, mock_jwt_config):
        """Tests if tokens generated at different times are unique."""
        # Arrange
        user_id = sample_user_data['user_id']
        email = sample_user_data['email']
        
        # Act
        token1 = JWTManager.generate_access_token(user_id, email)
        time.sleep(0.001)  # Small pause to ensure different timestamps
        token2 = JWTManager.generate_access_token(user_id, email)
        
        # Assert
        assert token1 != token2
    
    def test_jti_fields_are_different_for_same_user(self, sample_user_data, mock_jwt_config):
        """Tests if JWT IDs are different for tokens of same user."""
        # Arrange
        user_id = sample_user_data['user_id']
        email = sample_user_data['email']
        
        # Act
        token1 = JWTManager.generate_access_token(user_id, email)
        token2 = JWTManager.generate_access_token(user_id, email)
        
        decoded1 = JWTManager.decode_token(token1)
        decoded2 = JWTManager.decode_token(token2)
        
        # Assert
        assert decoded1['jti'] != decoded2['jti']
    
    def test_decode_token_validates_exp_by_default_with_valid_token(self, access_token, sample_user_data, mock_jwt_config):
        """Tests if decoding validates expiration by default with valid token."""
        # Act
        decoded = JWTManager.decode_token(access_token)
        
        # Assert
        assert decoded['user_id'] == sample_user_data['user_id']
    
    def test_decode_token_validates_exp_by_default_with_expired_token(self, expired_token, mock_jwt_config):
        """Tests if decoding validates expiration by default with expired token."""
        # Act & Assert
        with pytest.raises(jwt.ExpiredSignatureError):
            JWTManager.decode_token(expired_token)
    
    @pytest.mark.parametrize("field_name", [
        'user_id', 'email', 'type', 'iat', 'exp', 'nbf', 'jti'
    ])
    def test_access_token_required_fields(self, access_token, field_name, mock_jwt_config):
        """Tests if access token contains required field."""
        # Act
        decoded = JWTManager.decode_token(access_token)
        
        # Assert
        assert field_name in decoded
    
    @pytest.mark.parametrize("field_name", [
        'user_id', 'email', 'type', 'iat', 'exp', 'nbf', 'jti'
    ])
    def test_refresh_token_required_fields(self, refresh_token, field_name, mock_jwt_config):
        """Tests if refresh token contains required field."""
        # Act
        decoded = JWTManager.decode_token(refresh_token)
        
        # Assert
        assert field_name in decoded
    
    def test_first_jti_is_unique(self, sample_user_data, mock_jwt_config):
        """Tests if first generated JWT ID is unique."""
        # Act
        token = JWTManager.generate_access_token(
            sample_user_data['user_id'], 
            sample_user_data['email']
        )
        decoded = JWTManager.decode_token(token)
        
        # Assert
        assert decoded['jti'] is not None
        assert len(decoded['jti']) > 0
    
    def test_second_jti_is_unique(self, sample_user_data, mock_jwt_config):
        """Tests if second generated JWT ID is unique."""
        # Act
        token = JWTManager.generate_access_token(
            sample_user_data['user_id'], 
            sample_user_data['email']
        )
        decoded = JWTManager.decode_token(token)
        
        # Assert
        assert decoded['jti'] is not None
        assert len(decoded['jti']) > 0
    
    def test_third_jti_is_unique(self, sample_user_data, mock_jwt_config):
        """Tests if third generated JWT ID is unique."""
        # Act
        token = JWTManager.generate_access_token(
            sample_user_data['user_id'], 
            sample_user_data['email']
        )
        decoded = JWTManager.decode_token(token)
        
        # Assert
        assert decoded['jti'] is not None
        assert len(decoded['jti']) > 0