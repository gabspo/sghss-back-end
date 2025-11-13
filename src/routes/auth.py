"""Authentication routes blueprint."""

import logging

from flask import Blueprint, request

from ..exceptions import SGHSSException
from ..services.usuario_service import UsuarioService
from ..utils.response import ResponseFormatter

logger = logging.getLogger(__name__)

# Create blueprint
auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

# Initialize service
usuario_service = UsuarioService()


@auth_bp.route("/login", methods=["POST"])
def login():
    """Authenticate user and return access token."""
    try:
        data = request.get_json()

        email = data.get("email")
        senha = data.get("senha")

        if not email or not senha:
            return ResponseFormatter.error(
                message="Email and password are required",
                error_code="VALIDATION_ERROR",
                status_code=400,
            )

        usuario, token = usuario_service.autenticar(email, senha)

        response_data = usuario.to_dict()
        response_data["token"] = token

        return ResponseFormatter.success(
            data=response_data,
            message="Login successful",
        )

    except SGHSSException as e:
        return ResponseFormatter.error(
            message=e.message,
            error_code="AUTH_ERROR",
            status_code=e.status_code,
        )
    except Exception as e:
        logger.error(f"Unexpected error during login: {e}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )


@auth_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return ResponseFormatter.success(
        data={"status": "healthy"},
        message="Server is running",
    )
