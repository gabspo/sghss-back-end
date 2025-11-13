"""Consulta routes blueprint."""

import logging

from flask import Blueprint, request

from ..exceptions import SGHSSException
from ..services.consulta_service import ConsultaService
from ..utils.response import ResponseFormatter
from flask_jwt_extended import jwt_required

logger = logging.getLogger(__name__)

# Create blueprint
consulta_bp = Blueprint("consultas", __name__, url_prefix="/api/consultas")

# Initialize service
consulta_service = ConsultaService()


@consulta_bp.route("", methods=["POST"])
@jwt_required()
def criar_consulta():
    """Create a new consultation."""
    try:
        data = request.get_json()

        consulta = consulta_service.criar_consulta(
            paciente_id=data.get("paciente_id"),
            data=data.get("data"),
            motivo=data.get("motivo"),
            observacoes=data.get("observacoes"),
            profissional_id=data.get("profissional_id"),
            tipo_consulta=data.get("tipo_consulta", "presencial"),
            link_video=data.get("link_video"),
        )

        return ResponseFormatter.success(
            data=consulta.to_dict(),
            message="Consulta created successfully",
            status_code=201,
        )

    except SGHSSException as e:
        return ResponseFormatter.error(
            message=e.message,
            error_code="CONSULTA_ERROR",
            status_code=e.status_code,
        )
    except Exception as e:
        logger.error(f"Unexpected error creating consulta: {e}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )


@consulta_bp.route("", methods=["GET"])
@jwt_required()
def listar_consultas():
    """List all consultations with pagination and optional filtering."""
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)
        paciente_id = request.args.get("paciente_id", type=int)

        offset = (page - 1) * per_page

        consultas = consulta_service.listar_consultas(
            limite=per_page, offset=offset, paciente_id=paciente_id
        )

        return ResponseFormatter.success(
            data=[c.to_dict() for c in consultas],
            message="Consultas listed successfully",
        )

    except SGHSSException as e:
        return ResponseFormatter.error(
            message=e.message,
            error_code="CONSULTA_ERROR",
            status_code=e.status_code,
        )
    except Exception as e:
        logger.error(f"Unexpected error listing consultas: {e}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )


@consulta_bp.route("<int:consulta_id>", methods=["GET"])
@jwt_required()
def obter_consulta(consulta_id: int):
    """Get a consultation by ID."""
    try:
        consulta = consulta_service.obter_consulta_por_id(consulta_id)

        return ResponseFormatter.success(
            data=consulta.to_dict(),
            message="Consulta retrieved successfully",
        )

    except SGHSSException as e:
        return ResponseFormatter.error(
            message=e.message,
            error_code="CONSULTA_ERROR",
            status_code=e.status_code,
        )
    except Exception as e:
        logger.error(f"Unexpected error getting consulta: {e}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )


@consulta_bp.route("<int:consulta_id>", methods=["PUT"])
@jwt_required()
def atualizar_consulta(consulta_id: int):
    """Update a consultation."""
    try:
        data = request.get_json()

        consulta = consulta_service.atualizar_consulta(
            consulta_id=consulta_id,
            data=data.get("data"),
            motivo=data.get("motivo"),
            observacoes=data.get("observacoes"),
            link_video=data.get("link_video"),
        )

        return ResponseFormatter.success(
            data=consulta.to_dict(),
            message="Consulta updated successfully",
        )

    except SGHSSException as e:
        return ResponseFormatter.error(
            message=e.message,
            error_code="CONSULTA_ERROR",
            status_code=e.status_code,
        )
    except Exception as e:
        logger.error(f"Unexpected error updating consulta: {e}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )


@consulta_bp.route("<int:consulta_id>", methods=["DELETE"])
@jwt_required()
def deletar_consulta(consulta_id: int):
    """Delete a consultation."""
    try:
        consulta_service.deletar_consulta(consulta_id)

        return ResponseFormatter.success(
            message="Consulta deleted successfully",
        )

    except SGHSSException as e:
        return ResponseFormatter.error(
            message=e.message,
            error_code="CONSULTA_ERROR",
            status_code=e.status_code,
        )
    except Exception as e:
        logger.error(f"Unexpected error deleting consulta: {e}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )
