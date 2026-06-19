"""
HelperFunctions — Shared utility functions used across modules.
"""

import uuid
from datetime import datetime, timezone


def generate_id(prefix: str = "") -> str:
    """Generate a unique ID with optional prefix."""
    unique = str(uuid.uuid4())[:8]
    if prefix:
        return f"{prefix}_{unique}"
    return unique


def get_timestamp() -> str:
    """Return current UTC timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def mask_voucher_code(code: str) -> str:
    """Mask a voucher code, showing only last 4 characters."""
    if len(code) <= 4:
        return code
    return "****-****-" + code[-4:]
