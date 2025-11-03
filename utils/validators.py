"""
Input Validation Utilities
Common validation functions for API requests
"""

import re


def validate_email(email: str) -> tuple[bool, str]:
    """
    Validate email format

    Args:
        email (str): Email address to validate

    Returns:
        tuple: (is_valid, error_message)

    Example:
        >>> validate_email("user@example.com")
        (True, None)
        >>> validate_email("invalid-email")
        (False, 'Invalid email format')
    """
    if not email:
        return False, "Email is required"

    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not re.match(pattern, email):
        return False, "Invalid email format"

    if len(email) > 255:
        return False, "Email must not exceed 255 characters"

    return True, None


def validate_password(password: str) -> tuple[bool, str]:
    """
    Validate password strength

    Args:
        password (str): Password to validate

    Returns:
        tuple: (is_valid, error_message)

    Example:
        >>> validate_password("securePass123")
        (True, None)
        >>> validate_password("weak")
        (False, 'Password must be at least 6 characters long')
    """
    if not password:
        return False, "Password is required"

    if len(password) < 6:
        return False, "Password must be at least 6 characters long"

    if len(password) > 100:
        return False, "Password must not exceed 100 characters"

    return True, None


def validate_category_data(data: dict, is_update: bool = False) -> tuple[bool, str]:
    """
    Validate category data for POST and PUT requests

    Args:
        data (dict): Category data to validate
        is_update (bool): Whether this is an update operation

    Returns:
        tuple: (is_valid, error_message)
    """
    if not is_update and 'name' not in data:
        return False, "Field 'name' is required"

    if 'name' in data:
        if not data['name'] or not isinstance(data['name'], str):
            return False, "Field 'name' must be a non-empty string"
        if len(data['name']) > 100:
            return False, "Field 'name' must not exceed 100 characters"

    if 'description' in data and data['description'] is not None:
        if not isinstance(data['description'], str):
            return False, "Field 'description' must be a string"

    if 'is_active' in data and data['is_active'] is not None:
        if not isinstance(data['is_active'], bool):
            return False, "Field 'is_active' must be a boolean"

    return True, None
