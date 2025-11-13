"""Custom exceptions for SGHSS application."""


class SGHSSException(Exception):
    """Base exception for SGHSS application."""

    def __init__(self, message: str, status_code: int = 400):
        """
        Initialize the exception.

        Args:
            message: Exception message.
            status_code: HTTP status code.
        """
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ValidationError(SGHSSException):
    """Raised when validation fails."""

    def __init__(self, message: str):
        """
        Initialize the validation error.

        Args:
            message: Error message.
        """
        super().__init__(message, status_code=400)


class AuthenticationError(SGHSSException):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Invalid credentials"):
        """
        Initialize the authentication error.

        Args:
            message: Error message.
        """
        super().__init__(message, status_code=401)


class AuthorizationError(SGHSSException):
    """Raised when user is not authorized."""

    def __init__(self, message: str = "Unauthorized access"):
        """
        Initialize the authorization error.

        Args:
            message: Error message.
        """
        super().__init__(message, status_code=403)


class NotFoundError(SGHSSException):
    """Raised when a resource is not found."""

    def __init__(self, message: str = "Resource not found"):
        """
        Initialize the not found error.

        Args:
            message: Error message.
        """
        super().__init__(message, status_code=404)


class ConflictError(SGHSSException):
    """Raised when there is a conflict."""

    def __init__(self, message: str = "Resource already exists"):
        """
        Initialize the conflict error.

        Args:
            message: Error message.
        """
        super().__init__(message, status_code=409)


class DatabaseError(SGHSSException):
    """Raised when a database error occurs."""

    def __init__(self, message: str = "Database operation failed"):
        """
        Initialize the database error.

        Args:
            message: Error message.
        """
        super().__init__(message, status_code=500)
