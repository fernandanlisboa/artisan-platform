import jwt
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional
import time
import uuid
from app.common.config import config_by_name
import os


class JWTManager:
    """Class to manage JWT operations."""
    
    @staticmethod
    def _get_config():
        """Gets the current configuration consistently."""
        config_name = os.getenv('API_ENV', 'development')
        return config_by_name[config_name]
    
    @staticmethod
    def generate_access_token(user_id: str, email: str, **extra_claims) -> str:
        """
        Generates a JWT access token.
        
        Args:
            user_id: User ID
            email: User email
            **extra_claims: Additional claims to include in token
            
        Returns:
            str: Encoded JWT token
        """
        config = JWTManager._get_config()
        now = datetime.now(timezone.utc)
        expires = now + timedelta(minutes=config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        
        # Add unique identifier to ensure tokens are different
        jti = str(uuid.uuid4())  # Unique JWT ID
        
        payload = {
            'user_id': user_id,
            'email': email,
            'type': 'access',
            'jti': jti,  # JWT ID for uniqueness
            'iat': now.timestamp(),  # issued at - use timestamp for better precision
            'exp': expires.timestamp(),  # expiration time
            'nbf': now.timestamp(),  # not before
            **extra_claims  # Additional claims
        }
        
        return jwt.encode(
            payload,
            config.JWT_SECRET_KEY,
            algorithm=config.JWT_ALGORITHM
        )
    
    @staticmethod
    def generate_refresh_token(user_id: str, email: str) -> str:
        """
        Generates a JWT refresh token.
        
        Args:
            user_id: User ID
            email: User email
            
        Returns:
            str: Encoded JWT refresh token
        """
        config = JWTManager._get_config()
        now = datetime.now(timezone.utc)
        expires = now + timedelta(days=config.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
        
        # Add unique identifier to ensure tokens are different
        jti = str(uuid.uuid4())  # Unique JWT ID
        
        payload = {
            'user_id': user_id,
            'email': email,
            'type': 'refresh',
            'jti': jti,  # JWT ID for uniqueness
            'iat': now.timestamp(),  # issued at
            'exp': expires.timestamp(),  # expiration time
            'nbf': now.timestamp()  # not before
        }
        
        return jwt.encode(
            payload,
            config.JWT_SECRET_KEY,
            algorithm=config.JWT_ALGORITHM
        )
    
    @staticmethod
    def decode_token(token: str) -> Dict[str, Any]:
        """
        Decodes and validates a JWT token.
        
        Args:
            token: JWT token to decode
            
        Returns:
            Dict: Decoded token payload
            
        Raises:
            jwt.ExpiredSignatureError: If token has expired
            jwt.InvalidTokenError: If token is invalid
        """
        config = JWTManager._get_config()
        return jwt.decode(
            token,
            config.JWT_SECRET_KEY,
            algorithms=[config.JWT_ALGORITHM]
        )
    
    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Verifies if a token is valid without raising exceptions.
        
        Args:
            token: JWT token to verify
            
        Returns:
            Dict or None: Payload if valid, None if invalid
        """
        try:
            return JWTManager.decode_token(token)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None