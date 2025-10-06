from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class LoginRequest(BaseModel):
    """DTO para requisição de login."""
    model_config = ConfigDict(
        extra='forbid',  # Forbid extra fields
        validate_assignment=True,  # Validate on assignment
        protected_namespaces=(),  # No protected namespaces
        arbitrary_types_allowed=True  # Allow arbitrary types
    )
    
    email: str = Field(..., description="User email for login")
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
    token: Optional[str] = Field(None, description="Authentication token (e.g., JWT)")