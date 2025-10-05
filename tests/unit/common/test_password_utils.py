import pytest
from app.common.password_utils import hash_password, verify_password

class TestPasswordUtils:
    def test_password_hashing(self):
        """Test that passwords are properly hashed with Argon2."""
        # Arrange
        plain_password = "SecureP@ss123"
        
        # Act
        hashed = hash_password(plain_password)
        
        # Assert
        assert hashed != plain_password
        assert hashed.startswith("$argon2")  # Check it's an Argon2 hash
        
    def test_password_verification(self):
        """Test that Argon2 hashed passwords can be verified."""
        # Arrange
        plain_password = "SecureP@ss123"
        hashed = hash_password(plain_password)
        
        # Act & Assert
        assert verify_password(plain_password, hashed) is True
        assert verify_password("WrongPassword", hashed) is False