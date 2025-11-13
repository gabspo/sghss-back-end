"""Prescricao routes blueprint."""

import logging

from flask import Blueprint, request

from ..exceptions import SGHSSException
from ..services.prescricao_service import PrescricaoService
from ..utils.response import ResponseFormatter
from flask_jwt_extended import jwt_required

logger = logging.getLogger(__name__)

# Create blueprint
prescricao_bp = Blueprint("prescricoes", __name__, url_prefix="/api/prescricoes")

# Initialize service
prescricao_service = PrescricaoService()


@prescricao_bp.route("", methods=["POST"])
@jwt_required()
def criar_prescricao():
    """Create a new prescription."""
    try:
        data = request.get_json()

        prescricao = prescricao_service.criar_prescricao(
            consulta_id=data.get("consulta_id"),
            medicamento_id=data.get("medicamento_id"),
            duracao=data.get("duracao"),
            instrucoes=data.get("instrucoes"),
        )

        return ResponseFormatter.success(
            data=prescricao.to_dict(),
            message="Prescricao created successfully",
            status_code=201,
        )

    except SGHSSException as e:
        return ResponseFormatter.error(
            message=e.message,
            error_code="PRESCRICAO_ERROR",
            status_code=e.status_code,
        )
    except Exception as e:
        logger.error(f"Unexpected error creating prescricao: {e}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )


@prescricao_bp.route("", methods=["GET"])
@jwt_required()
def listar_prescricoes():
    """List all prescriptions with pagination."""
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)

        offset = (page - 1) * per_page

        prescricoes = prescricao_service.listar_prescricoes(
            limite=per_page, offset=offset
        )

        return ResponseFormatter.success(
            data=[p.to_dict() for p in prescricoes],
            message="Prescricoes listed successfully",
        )

    except SGHSSException as e:
        return ResponseFormatter.error(
            message=e.message,
            error_code="PRESCRICAO_ERROR",
            status_code=e.status_code,
        )
    except Exception as e:
        logger.error(f"Unexpected error listing prescricoes: {e}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )


@prescricao_bp.route("<int:prescricao_id>", methods=["GET"])
@jwt_required()
def obter_prescricao(prescricao_id: int):
    """Get a prescription by ID."""
    try:
        prescricao = prescricao_service.obter_prescricao_por_id(prescricao_id)

        return ResponseFormatter.success(
            data=prescricao.to_dict(),
            message="Prescricao retrieved successfully",
        )

    except SGHSSException as e:
        return ResponseFormatter.error(
            message=e.message,
            error_code="PRESCRICAO_ERROR",
            status_code=e.status_code,
        )
    except Exception as e:
        logger.error(f"Unexpected error getting prescricao: {e}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )


@prescricao_bp.route("consulta/<int:consulta_id>", methods=["GET"])
@jwt_required()
def listar_prescricoes_por_consulta(consulta_id: int):
    """List prescriptions for a specific consultation."""
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)

        offset = (page - 1) * per_page

        prescricoes = prescricao_service.listar_prescricoes_por_consulta(
            consulta_id=consulta_id, limite=per_page, offset=offset
        )

        return ResponseFormatter.success(
            data=[p.to_dict() for p in prescricoes],
            message="Prescricoes listed successfully",
        )

    except SGHSSException as e:
        return ResponseFormatter.error(
            message=e.message,
            error_code="PRESCRICAO_ERROR",
            status_code=e.status_code,
        )
    except Exception as e:
        logger.error(f"Unexpected error listing prescricoes: {e}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )


@prescricao_bp.route("<int:prescricao_id>", methods=["PUT"])
@jwt_required()
def atualizar_prescricao(prescricao_id: int):
    """Update a prescription."""
    try:
        data = request.get_json()

        prescricao = prescricao_service.atualizar_prescricao(
            prescricao_id=prescricao_id,
            duracao=data.get("duracao"),
            instrucoes=data.get("instrucoes"),
        )

        return ResponseFormatter.success(
            data=prescricao.to_dict(),
            message="Prescricao updated successfully",
        )

    except SGHSSException as e:
        return ResponseFormatter.error(
            message=e.message,
            error_code="PRESCRICAO_ERROR",
            status_code=e.status_code,
        )
    except Exception as e:
        logger.error(f"Unexpected error updating prescricao: {e}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )


@prescricao_bp.route("<int:prescricao_id>", methods=["DELETE"])
@jwt_required()
def deletar_prescricao(prescricao_id: int):
    """Delete a prescription."""
    try:
        prescricao_service.deletar_prescricao(prescricao_id)

        return ResponseFormatter.success(
            message="Prescricao deleted successfully",
        )

    except SGHSSException as e:
        return ResponseFormatter.error(
            message=e.message,
            error_code="PRESCRICAO_ERROR",
            status_code=e.status_code,
        )
    except Exception as e:
        logger.error(f"Unexpected error deleting prescricao: {e}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )
