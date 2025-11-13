"""Paciente routes blueprint."""

import logging

from flask import Blueprint, request

from ..exceptions import SGHSSException
from ..services.paciente_service import PacienteService
from ..utils.response import ResponseFormatter
from flask_jwt_extended import jwt_required

logger = logging.getLogger(__name__)

# Create blueprint
paciente_bp = Blueprint("pacientes", __name__, url_prefix="/api/pacientes")

# Initialize service
paciente_service = PacienteService()


@paciente_bp.route("", methods=["POST"])
@jwt_required()
def criar_paciente():
    """Create a new patient."""
    try:
        data = request.get_json()

        paciente = paciente_service.criar_paciente(
            nome=data.get("nome"),
            email=data.get("email"),
            telefone=data.get("telefone"),
            cpf=data.get("cpf"),
            data_nascimento=data.get("data_nascimento"),
            endereco=data.get("endereco"),
        )

        return ResponseFormatter.success(
            data=paciente.to_dict(),
            message="Paciente created successfully",
            status_code=201,
        )

    except SGHSSException as e:
        return ResponseFormatter.error(
            message=e.message,
            error_code="PACIENTE_ERROR",
            status_code=e.status_code,
        )
    except Exception as e:
        logger.error(f"Unexpected error creating paciente: {e}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )


@paciente_bp.route("", methods=["GET"])
@jwt_required()
def listar_pacientes():
    """List all patients with pagination."""
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)

        offset = (page - 1) * per_page

        pacientes = paciente_service.listar_pacientes(limite=per_page, offset=offset)

        return ResponseFormatter.success(
            data=[p.to_dict() for p in pacientes],
            message="Pacientes listed successfully",
        )

    except SGHSSException as e:
        return ResponseFormatter.error(
            message=e.message,
            error_code="PACIENTE_ERROR",
            status_code=e.status_code,
        )
    except Exception as e:
        logger.error(f"Unexpected error listing pacientes: {e}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )


@paciente_bp.route("<int:paciente_id>", methods=["GET"])
@jwt_required()
def obter_paciente(paciente_id: int):
    """Get a patient by ID."""
    try:
        paciente = paciente_service.obter_paciente_por_id(paciente_id)

        return ResponseFormatter.success(
            data=paciente.to_dict(),
            message="Paciente retrieved successfully",
        )

    except SGHSSException as e:
        return ResponseFormatter.error(
            message=e.message,
            error_code="PACIENTE_ERROR",
            status_code=e.status_code,
        )
    except Exception as e:
        logger.error(f"Unexpected error getting paciente: {e}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )


@paciente_bp.route("<int:paciente_id>", methods=["PUT"])
@jwt_required()
def atualizar_paciente(paciente_id: int):
    """Update a patient."""
    try:
        data = request.get_json()

        paciente = paciente_service.atualizar_paciente(
            paciente_id=paciente_id,
            nome=data.get("nome"),
            email=data.get("email"),
            telefone=data.get("telefone"),
            endereco=data.get("endereco"),
        )

        return ResponseFormatter.success(
            data=paciente.to_dict(),
            message="Paciente updated successfully",
        )

    except SGHSSException as e:
        return ResponseFormatter.error(
            message=e.message,
            error_code="PACIENTE_ERROR",
            status_code=e.status_code,
        )
    except Exception as e:
        logger.error(f"Unexpected error updating paciente: {e}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )


@paciente_bp.route("<int:paciente_id>", methods=["DELETE"])
@jwt_required()
def deletar_paciente(paciente_id: int):
    """Delete a patient."""
    try:
        paciente_service.deletar_paciente(paciente_id)

        return ResponseFormatter.success(
            message="Paciente deleted successfully",
        )

    except SGHSSException as e:
        return ResponseFormatter.error(
            message=e.message,
            error_code="PACIENTE_ERROR",
            status_code=e.status_code,
        )
    except Exception as e:
        logger.error(f"Unexpected error deleting paciente: {e}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )
