"""Response utilities for SGHSS application."""

from typing import Any, Dict, Optional

from flask import jsonify, Response


class ResponseFormatter:
    """Utility class for formatting API responses."""

    @staticmethod
    def success(
        data: Any = None,
        message: str = "Success",
        status_code: int = 200,
    ) -> tuple[Response, int]:
        """
        Create a success response.

        Args:
            data: Response data.
            message: Response message.
            status_code: HTTP status code.

        Returns:
            Tuple of (Flask Response, HTTP status code).
        """
        response = {
            "status": "success",
            "message": message,
            "data": data,
        }
        return jsonify(response), status_code

    @staticmethod
    def error(
        message: str = "Error",
        error_code: str = "INTERNAL_ERROR",
        status_code: int = 400,
        details: Optional[Dict[str, Any]] = None,
    ) -> tuple[Response, int]:
        """
        Create an error response.

        Args:
            message: Error message.
            error_code: Error code identifier.
            status_code: HTTP status code.
            details: Additional error details.

        Returns:
            Tuple of (Flask Response, HTTP status code).
        """
        response = {
            "status": "error",
            "message": message,
            "error_code": error_code,
            "details": details,
        }
        return jsonify(response), status_code

    @staticmethod
    def paginated(
        data: list,
        total: int,
        page: int,
        per_page: int,
        message: str = "Success",
        status_code: int = 200,
    ) -> tuple[Response, int]:
        """
        Create a paginated response.

        Args:
            data: List of items.
            total: Total number of items.
            page: Current page number.
            per_page: Items per page.
            message: Response message.
            status_code: HTTP status code.

        Returns:
            Tuple of (Flask Response, HTTP status code).
        """
        total_pages = (total + per_page - 1) // per_page
        response = {
            "status": "success",
            "message": message,
            "data": data,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "total_pages": total_pages,
            },
        }
        return jsonify(response), status_code
