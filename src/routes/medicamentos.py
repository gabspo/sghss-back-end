"""Medicamento routes blueprint."""

import logging

from flask import Blueprint, request

from ..exceptions import SGHSSException
from ..services.medicamento_service import MedicamentoService
from ..utils.response import ResponseFormatter
from flask_jwt_extended import jwt_required

logger = logging.getLogger(__name__)

# Create blueprint
medicamento_bp = Blueprint("medicamentos", __name__, url_prefix="/api/medicamentos")

# Initialize service
medicamento_service = MedicamentoService()


@medicamento_bp.route("", methods=["POST"])
@jwt_required()
def criar_medicamento():
    """Create a new medication."""
    try:
        data = request.get_json()

        medicamento = medicamento_service.criar_medicamento(
            nome=data.get("nome"),
            descricao=data.get("descricao"),
            dosagem=data.get("dosagem"),
        )

        return ResponseFormatter.success(
            data=medicamento.to_dict(),
            message="Medicamento created successfully",
            status_code=201,
        )

    except SGHSSException as e:
        return ResponseFormatter.error(
            message=e.message,
            error_code="MEDICAMENTO_ERROR",
            status_code=e.status_code,
        )
    except Exception as e:
        logger.error(f"Unexpected error creating medicamento: {e}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )


@medicamento_bp.route("", methods=["GET"])
@jwt_required()
def listar_medicamentos():
    """List all medications with pagination."""
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)
        busca = request.args.get("busca", type=str)

        offset = (page - 1) * per_page

        if busca:
            medicamentos = medicamento_service.buscar_medicamentos_por_nome(
                nome=busca, limite=per_page, offset=offset
            )
        else:
            medicamentos = medicamento_service.listar_medicamentos(
                limite=per_page, offset=offset
            )

        return ResponseFormatter.success(
            data=[m.to_dict() for m in medicamentos],
            message="Medicamentos listed successfully",
        )

    except SGHSSException as e:
        return ResponseFormatter.error(
            message=e.message,
            error_code="MEDICAMENTO_ERROR",
            status_code=e.status_code,
        )
    except Exception as e:
        logger.error(f"Unexpected error listing medicamentos: {e}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )


@medicamento_bp.route("<int:medicamento_id>", methods=["GET"])
@jwt_required()
def obter_medicamento(medicamento_id: int):
    """Get a medication by ID."""
    try:
        medicamento = medicamento_service.obter_medicamento_por_id(medicamento_id)

        return ResponseFormatter.success(
            data=medicamento.to_dict(),
            message="Medicamento retrieved successfully",
        )

    except SGHSSException as e:
        return ResponseFormatter.error(
            message=e.message,
            error_code="MEDICAMENTO_ERROR",
            status_code=e.status_code,
        )
    except Exception as e:
        logger.error(f"Unexpected error getting medicamento: {e}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )


@medicamento_bp.route("<int:medicamento_id>", methods=["PUT"])
@jwt_required()
def atualizar_medicamento(medicamento_id: int):
    """Update a medication."""
    try:
        data = request.get_json()

        medicamento = medicamento_service.atualizar_medicamento(
            medicamento_id=medicamento_id,
            nome=data.get("nome"),
            descricao=data.get("descricao"),
            dosagem=data.get("dosagem"),
        )

        return ResponseFormatter.success(
            data=medicamento.to_dict(),
            message="Medicamento updated successfully",
        )

    except SGHSSException as e:
        return ResponseFormatter.error(
            message=e.message,
            error_code="MEDICAMENTO_ERROR",
            status_code=e.status_code,
        )
    except Exception as e:
        logger.error(f"Unexpected error updating medicamento: {e}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )


@medicamento_bp.route("<int:medicamento_id>", methods=["DELETE"])
@jwt_required()
def deletar_medicamento(medicamento_id: int):
    """Delete a medication."""
    try:
        medicamento_service.deletar_medicamento(medicamento_id)

        return ResponseFormatter.success(
            message="Medicamento deleted successfully",
        )

    except SGHSSException as e:
        return ResponseFormatter.error(
            message=e.message,
            error_code="MEDICAMENTO_ERROR",
            status_code=e.status_code,
        )
    except Exception as e:
        logger.error(f"Unexpected error deleting medicamento: {e}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )
