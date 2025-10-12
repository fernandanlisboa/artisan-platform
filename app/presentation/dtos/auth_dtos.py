from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional


class LoginRequest(BaseModel):
    """DTO para requisição de login."""
    model_config = ConfigDict(
        extra='forbid',  # Forbid extra fields
        validate_assignment=True,  # Validate on assignment
        protected_namespaces=(),  # No protected namespaces
        arbitrary_types_allowed=True  # Allow arbitrary types
    )
    
    email: EmailStr = Field(..., description="User email for login")
    password: str = Field(..., description="User password for login")
    
class LoginResponse(BaseModel):
    """DTO para resposta de login."""
    model_config = ConfigDict(
        extra='forbid',  # Forbid extra fields
        validate_assignment=True,  # Validate on assignment
        protected_namespaces=(),  # No protected namespaces
        arbitrary_types_allowed=True  # Allow arbitrary types
    )
    
    user_id: str = Field(..., description="ID of the authenticated user")
    email: str = Field(..., description="Email of the authenticated user")
    access_token: str = Field(..., description="Access token for the authenticated user")
    refresh_token: str = Field(..., description="Refresh token for the authenticated user")
    token_type: str = Field("Bearer", description="Type of the token")
    expires_in: int = Field(..., description="Expiration time of the token in seconds")