"""Profissional routes blueprint."""

import logging

from flask import Blueprint, request

from ..exceptions import SGHSSException
from ..services.profissional_service import ProfissionalService
from ..utils.response import ResponseFormatter
from flask_jwt_extended import jwt_required

logger = logging.getLogger(__name__)

# Create blueprint
profissional_bp = Blueprint("profissionais", __name__, url_prefix="/api/profissionais")

# Initialize service
profissional_service = ProfissionalService()


@profissional_bp.route("", methods=["POST"])
@jwt_required()
def criar_profissional():
    """Create a new professional."""
    try:
        data = request.get_json()

        profissional = profissional_service.criar_profissional(
            nome=data.get("nome"),
            email=data.get("email"),
            telefone=data.get("telefone"),
            especialidade=data.get("especialidade"),
            registro=data.get("registro"),
        )

        return ResponseFormatter.success(
            data=profissional.to_dict(),
            message="Profissional created successfully",
            status_code=201,
        )

    except SGHSSException as e:
        return ResponseFormatter.error(
            message=e.message,
            error_code="PROFISSIONAL_ERROR",
            status_code=e.status_code,
        )
    except Exception as e:
        logger.error(f"Unexpected error creating profissional: {e}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )


@profissional_bp.route("", methods=["GET"])
@jwt_required()
def listar_profissionais():
    """List all professionals with pagination."""
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)

        offset = (page - 1) * per_page

        profissionais = profissional_service.listar_profissionais(
            limite=per_page, offset=offset
        )

        return ResponseFormatter.success(
            data=[p.to_dict() for p in profissionais],
            message="Profissionais listed successfully",
        )

    except SGHSSException as e:
        return ResponseFormatter.error(
            message=e.message,
            error_code="PROFISSIONAL_ERROR",
            status_code=e.status_code,
        )
    except Exception as e:
        logger.error(f"Unexpected error listing profissionais: {e}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )


@profissional_bp.route("<int:profissional_id>", methods=["GET"])
@jwt_required()
def obter_profissional(profissional_id: int):
    """Get a professional by ID."""
    try:
        profissional = profissional_service.obter_profissional_por_id(profissional_id)

        return ResponseFormatter.success(
            data=profissional.to_dict(),
            message="Profissional retrieved successfully",
        )

    except SGHSSException as e:
        return ResponseFormatter.error(
            message=e.message,
            error_code="PROFISSIONAL_ERROR",
            status_code=e.status_code,
        )
    except Exception as e:
        logger.error(f"Unexpected error getting profissional: {e}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )


@profissional_bp.route("<int:profissional_id>", methods=["PUT"])
@jwt_required()
def atualizar_profissional(profissional_id: int):
    """Update a professional."""
    try:
        data = request.get_json()

        profissional = profissional_service.atualizar_profissional(
            profissional_id=profissional_id,
            nome=data.get("nome"),
            email=data.get("email"),
            telefone=data.get("telefone"),
            especialidade=data.get("especialidade"),
        )

        return ResponseFormatter.success(
            data=profissional.to_dict(),
            message="Profissional updated successfully",
        )

    except SGHSSException as e:
        return ResponseFormatter.error(
            message=e.message,
            error_code="PROFISSIONAL_ERROR",
            status_code=e.status_code,
        )
    except Exception as e:
        logger.error(f"Unexpected error updating profissional: {e}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )


@profissional_bp.route("<int:profissional_id>", methods=["DELETE"])
@jwt_required()
def deletar_profissional(profissional_id: int):
    """Delete a professional."""
    try:
        profissional_service.deletar_profissional(profissional_id)

        return ResponseFormatter.success(
            message="Profissional deleted successfully",
        )

    except SGHSSException as e:
        return ResponseFormatter.error(
            message=e.message,
            error_code="PROFISSIONAL_ERROR",
            status_code=e.status_code,
        )
    except Exception as e:
        logger.error(f"Unexpected error deleting profissional: {e}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )
