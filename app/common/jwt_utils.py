import jwt
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional
from app.common.config import config_by_name
import os

# Obter configuração atual
config_name = os.getenv('API_ENV', 'development')
config = config_by_name[config_name]

class JWTManager:
    """Classe para gerenciar operações JWT."""
    
    @staticmethod
    def generate_access_token(user_id: str, email: str, **extra_claims) -> str:
        """
        Gera um token JWT de acesso.
        
        Args:
            user_id: ID do usuário
            email: Email do usuário
            **extra_claims: Claims adicionais para incluir no token
            
        Returns:
            str: Token JWT codificado
        """
        now = datetime.now(timezone.utc)
        expires = now + timedelta(minutes=config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        
        payload = {
            'user_id': user_id,
            'email': email,
            'type': 'access',
            'iat': now,  # issued at
            'exp': expires,  # expiration time
            'nbf': now,  # not before
            **extra_claims  # Claims adicionais
        }
        
        return jwt.encode(
            payload,
            config.JWT_SECRET_KEY,
            algorithm=config.JWT_ALGORITHM
        )
    
    @staticmethod
    def generate_refresh_token(user_id: str, email: str) -> str:
        """
        Gera um token JWT de refresh.
        
        Args:
            user_id: ID do usuário
            email: Email do usuário
            
        Returns:
            str: Token JWT de refresh codificado
        """
        now = datetime.now(timezone.utc)
        expires = now + timedelta(days=config.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
        
        payload = {
            'user_id': user_id,
            'email': email,
            'type': 'refresh',
            'iat': now,
            'exp': expires,
            'nbf': now
        }
        
        return jwt.encode(
            payload,
            config.JWT_SECRET_KEY,
            algorithm=config.JWT_ALGORITHM
        )
    
    @staticmethod
    def decode_token(token: str) -> Dict[str, Any]:
        """
        Decodifica e valida um token JWT.
        
        Args:
            token: Token JWT para decodificar
            
        Returns:
            Dict: Payload do token decodificado
            
        Raises:
            jwt.ExpiredSignatureError: Se o token expirou
            jwt.InvalidTokenError: Se o token é inválido
        """
        return jwt.decode(
            token,
            config.JWT_SECRET_KEY,
            algorithms=[config.JWT_ALGORITHM]
        )
    
    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Verifica se um token é válido sem lançar exceções.
        
        Args:
            token: Token JWT para verificar
            
        Returns:
            Dict ou None: Payload se válido, None se inválido
        """
        try:
            return JWTManager.decode_token(token)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None