from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Create a global PasswordHasher instance with secure defaults
_password_hasher = PasswordHasher(
    time_cost=3,       # Number of iterations
    memory_cost=65536, # Memory usage in kibibytes (64 MB)
    parallelism=4,     # Degree of parallelism
    hash_len=32,       # Length of the hash in bytes
    salt_len=16        # Length of the random salt in bytes
)

def hash_password(plain_password: str) -> str:
    """
    Hashes a plain text password using Argon2id.
    
    Args:
        plain_password: The plain text password to hash
        
    Returns:
        str: The hashed password as a string (includes algorithm, salt, etc.)
    """
    return _password_hasher.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if the provided plain text password matches the hashed password.
    
    Args:
        plain_password: The plain text password to check
        hashed_password: The hashed password to check against
        
    Returns:
        bool: True if the password matches, False otherwise
    """
    try:
        _password_hasher.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        return False