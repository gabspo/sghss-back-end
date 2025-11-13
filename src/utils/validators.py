"""Validation utilities for SGHSS application."""

import re
from typing import Any, Dict, List

from ..exceptions import ValidationError


class Validator:
    """Utility class for data validation."""

    @staticmethod
    def validate_required_fields(data: Dict[str, Any], required: List[str]) -> None:
        """
        Validate that required fields are present in data.

        Args:
            data: Data dictionary to validate.
            required: List of required field names.

        Raises:
            ValidationError: If required fields are missing.
        """
        missing = [field for field in required if field not in data or not data[field]]
        if missing:
            raise ValidationError(f"Missing required fields: {', '.join(missing)}")

    @staticmethod
    def validate_email(email: str) -> None:
        """
        Validate email format.

        Args:
            email: Email address to validate.

        Raises:
            ValidationError: If email format is invalid.
        """
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, email):
            raise ValidationError("Invalid email format")

    @staticmethod
    def validate_password_strength(password: str, min_length: int = 6) -> None:
        """
        Validate password strength.

        Args:
            password: Password to validate.
            min_length: Minimum password length.

        Raises:
            ValidationError: If password is too weak.
        """
        if len(password) < min_length:
            raise ValidationError(f"Password must be at least {min_length} characters")

    @staticmethod
    def validate_phone(phone: str) -> None:
        """
        Validate phone number format.

        Args:
            phone: Phone number to validate.

        Raises:
            ValidationError: If phone format is invalid.
        """
        pattern = r"^\+?[0-9]{10,15}$"
        if not re.match(pattern, phone):
            raise ValidationError("Invalid phone number format")

    @staticmethod
    def validate_date_format(date_str: str, format_str: str = "%Y-%m-%d") -> None:
        """
        Validate date format.

        Args:
            date_str: Date string to validate.
            format_str: Expected date format.

        Raises:
            ValidationError: If date format is invalid.
        """
        from datetime import datetime

        try:
            datetime.strptime(date_str, format_str)
        except ValueError:
            raise ValidationError(f"Invalid date format. Expected: {format_str}")
