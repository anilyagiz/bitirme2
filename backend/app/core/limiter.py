"""Rate limiting configuration"""

from slowapi import Limiter
from slowapi.util import get_remote_address


def get_limiter() -> Limiter:
    """
    Create and configure rate limiter

    Returns:
        Configured Limiter instance
    """
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=["100/minute"],  # Default rate limit for all endpoints
        storage_uri="memory://",  # Use in-memory storage (can be replaced with Redis)
        strategy="fixed-window"
    )

    return limiter


# Global limiter instance
limiter = get_limiter()
