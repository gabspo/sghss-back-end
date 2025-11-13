"""Usuario routes blueprint."""

import logging
from typing import Optional

from flask import Blueprint, request, jsonify

from ..exceptions import SGHSSException
from ..services.usuario_service import UsuarioService
from ..utils.response import ResponseFormatter
from flask_jwt_extended import jwt_required, get_jwt_identity

logger = logging.getLogger(__name__)

# Create blueprint
usuario_bp = Blueprint("usuarios", __name__, url_prefix="/api/usuarios")

# Initialize service
usuario_service = UsuarioService()


@usuario_bp.route("", methods=["POST"])
def criar_usuario():
    """Create a new user."""
    try:
        data = request.get_json()

        usuario = usuario_service.criar_usuario(
            nome=data.get("nome"),
            email=data.get("email"),
            senha=data.get("senha"),
            tipo=data.get("tipo"),
        )

        return ResponseFormatter.success(
            data=usuario.to_dict(),
            message="Usuario created successfully",
            status_code=201,
        )

    except SGHSSException as e:
        return ResponseFormatter.error(
            message=e.message,
            error_code="USUARIO_ERROR",
            status_code=e.status_code,
        )
    except Exception as e:
        logger.error(f"Unexpected error creating usuario: {e}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )


@usuario_bp.route("", methods=["GET"])
@jwt_required()
def listar_usuarios():
    """List all users with pagination."""
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)

        offset = (page - 1) * per_page

        usuarios = usuario_service.listar_usuarios(limite=per_page, offset=offset)

        return ResponseFormatter.success(
            data=[u.to_dict() for u in usuarios],
            message="Usuarios listed successfully",
        )

    except SGHSSException as e:
        return ResponseFormatter.error(
            message=e.message,
            error_code="USUARIO_ERROR",
            status_code=e.status_code,
        )
    except Exception as e:
        logger.error(f"Unexpected error listing usuarios: {e}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )


@usuario_bp.route("<int:usuario_id>", methods=["GET"])
@jwt_required()
def obter_usuario(usuario_id: int):
    """Get a user by ID."""
    try:
        usuario = usuario_service.obter_usuario_por_id(usuario_id)

        return ResponseFormatter.success(
            data=usuario.to_dict(),
            message="Usuario retrieved successfully",
        )

    except SGHSSException as e:
        return ResponseFormatter.error(
            message=e.message,
            error_code="USUARIO_ERROR",
            status_code=e.status_code,
        )
    except Exception as e:
        logger.error(f"Unexpected error getting usuario: {e}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )


@usuario_bp.route("<int:usuario_id>", methods=["PUT"])
@jwt_required()
def atualizar_usuario(usuario_id: int):
    """Update a user."""
    try:
        data = request.get_json()

        usuario = usuario_service.atualizar_usuario(
            usuario_id=usuario_id,
            nome=data.get("nome"),
            email=data.get("email"),
            tipo=data.get("tipo"),
        )

        return ResponseFormatter.success(
            data=usuario.to_dict(),
            message="Usuario updated successfully",
        )

    except SGHSSException as e:
        return ResponseFormatter.error(
            message=e.message,
            error_code="USUARIO_ERROR",
            status_code=e.status_code,
        )
    except Exception as e:
        logger.error(f"Unexpected error updating usuario: {e}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )


@usuario_bp.route("<int:usuario_id>", methods=["DELETE"])
@jwt_required()
def deletar_usuario(usuario_id: int):
    """Delete a user."""
    try:
        usuario_service.deletar_usuario(usuario_id)

        return ResponseFormatter.success(
            message="Usuario deleted successfully",
        )

    except SGHSSException as e:
        return ResponseFormatter.error(
            message=e.message,
            error_code="USUARIO_ERROR",
            status_code=e.status_code,
        )
    except Exception as e:
        logger.error(f"Unexpected error deleting usuario: {e}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )
