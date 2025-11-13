"""Prescricao service for business logic."""

import logging
from typing import List

from ..config.database import get_db_manager
from ..exceptions import DatabaseError, NotFoundError, ValidationError
from ..models import Prescricao
from ..utils.validators import Validator

logger = logging.getLogger(__name__)


class PrescricaoService:
    """Service for prescricao-related operations."""

    def __init__(self):
        """Initialize prescricao service."""
        self.db_manager = get_db_manager()

    def criar_prescricao(
        self,
        consulta_id: int,
        medicamento_id: int,
        duracao: str = None,
        instrucoes: str = None,
    ) -> Prescricao:
        """
        Create a new prescription.

        Args:
            consulta_id: Consultation ID.
            medicamento_id: Medication ID.
            duracao: Duration of treatment.
            instrucoes: Instructions for use.

        Returns:
            Created Prescricao object.

        Raises:
            ValidationError: If validation fails.
            DatabaseError: If database operation fails.
        """
        # Validate inputs
        Validator.validate_required_fields(
            {
                "consulta_id": consulta_id,
                "medicamento_id": medicamento_id,
            },
            ["consulta_id", "medicamento_id"],
        )

        try:
            with self.db_manager.get_cursor() as (cursor, conn):
                cursor.execute(
                    """
                    INSERT INTO prescricoes (consulta_id, medicamento_id, duracao, instrucoes)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (consulta_id, medicamento_id, duracao, instrucoes),
                )
                conn.commit()
                prescricao_id = cursor.lastrowid

            logger.info(f"Prescricao created successfully: {prescricao_id}")
            return self.obter_prescricao_por_id(prescricao_id)

        except Exception as err:
            logger.error(f"Error creating prescricao: {err}")
            raise DatabaseError(f"Failed to create prescricao: {str(err)}")

    def listar_prescricoes(self, limite: int = 100, offset: int = 0) -> List[Prescricao]:
        """
        List all prescriptions with pagination.

        Args:
            limite: Number of records to fetch.
            offset: Number of records to skip.

        Returns:
            List of Prescricao objects.

        Raises:
            DatabaseError: If database operation fails.
        """
        try:
            with self.db_manager.get_cursor(dictionary=True) as (cursor, conn):
                cursor.execute(
                    """
                    SELECT id, consulta_id, medicamento_id, duracao, instrucoes
                    FROM prescricoes
                    LIMIT %s OFFSET %s
                    """,
                    (limite, offset),
                )
                prescricoes_data = cursor.fetchall()

            prescricoes = [
                self._map_to_prescricao(data) for data in prescricoes_data
            ]
            logger.info(f"Listed {len(prescricoes)} prescricoes")
            return prescricoes

        except Exception as err:
            logger.error(f"Error listing prescricoes: {err}")
            raise DatabaseError(f"Failed to list prescricoes: {str(err)}")

    def obter_prescricao_por_id(self, prescricao_id: int) -> Prescricao:
        """
        Get prescription by ID.

        Args:
            prescricao_id: Prescription ID.

        Returns:
            Prescricao object.

        Raises:
            NotFoundError: If prescription not found.
            DatabaseError: If database operation fails.
        """
        try:
            with self.db_manager.get_cursor(dictionary=True) as (cursor, conn):
                cursor.execute(
                    """
                    SELECT id, consulta_id, medicamento_id, duracao, instrucoes
                    FROM prescricoes
                    WHERE id = %s
                    """,
                    (prescricao_id,),
                )
                prescricao_data = cursor.fetchone()

            if not prescricao_data:
                raise NotFoundError("Prescricao not found")

            return self._map_to_prescricao(prescricao_data)

        except NotFoundError:
            raise
        except Exception as err:
            logger.error(f"Error getting prescricao: {err}")
            raise DatabaseError(f"Failed to get prescricao: {str(err)}")

    def listar_prescricoes_por_consulta(
        self, consulta_id: int, limite: int = 100, offset: int = 0
    ) -> List[Prescricao]:
        """
        List prescriptions for a specific consultation.

        Args:
            consulta_id: Consultation ID.
            limite: Number of records to fetch.
            offset: Number of records to skip.

        Returns:
            List of Prescricao objects.

        Raises:
            DatabaseError: If database operation fails.
        """
        try:
            with self.db_manager.get_cursor(dictionary=True) as (cursor, conn):
                cursor.execute(
                    """
                    SELECT id, consulta_id, medicamento_id, duracao, instrucoes
                    FROM prescricoes
                    WHERE consulta_id = %s
                    LIMIT %s OFFSET %s
                    """,
                    (consulta_id, limite, offset),
                )
                prescricoes_data = cursor.fetchall()

            prescricoes = [
                self._map_to_prescricao(data) for data in prescricoes_data
            ]
            logger.info(
                f"Listed {len(prescricoes)} prescricoes for consultation {consulta_id}"
            )
            return prescricoes

        except Exception as err:
            logger.error(f"Error listing prescricoes: {err}")
            raise DatabaseError(f"Failed to list prescricoes: {str(err)}")

    def atualizar_prescricao(
        self,
        prescricao_id: int,
        duracao: str = None,
        instrucoes: str = None,
    ) -> Prescricao:
        """
        Update prescription.

        Args:
            prescricao_id: Prescription ID.
            duracao: New duration.
            instrucoes: New instructions.

        Returns:
            Updated Prescricao object.

        Raises:
            NotFoundError: If prescription not found.
            DatabaseError: If database operation fails.
        """
        # Check if prescription exists
        self.obter_prescricao_por_id(prescricao_id)

        try:
            updates = []
            params = []

            if duracao is not None:
                updates.append("duracao = %s")
                params.append(duracao)
            if instrucoes is not None:
                updates.append("instrucoes = %s")
                params.append(instrucoes)

            if not updates:
                return self.obter_prescricao_por_id(prescricao_id)

            params.append(prescricao_id)

            with self.db_manager.get_cursor() as (cursor, conn):
                cursor.execute(
                    f"""
                    UPDATE prescricoes
                    SET {", ".join(updates)}
                    WHERE id = %s
                    """,
                    params,
                )
                conn.commit()

            logger.info(f"Prescricao {prescricao_id} updated successfully")
            return self.obter_prescricao_por_id(prescricao_id)

        except Exception as err:
            logger.error(f"Error updating prescricao: {err}")
            raise DatabaseError(f"Failed to update prescricao: {str(err)}")

    def deletar_prescricao(self, prescricao_id: int) -> None:
        """
        Delete prescription.

        Args:
            prescricao_id: Prescription ID.

        Raises:
            NotFoundError: If prescription not found.
            DatabaseError: If database operation fails.
        """
        # Check if prescription exists
        self.obter_prescricao_por_id(prescricao_id)

        try:
            with self.db_manager.get_cursor() as (cursor, conn):
                cursor.execute(
                    "DELETE FROM prescricoes WHERE id = %s", (prescricao_id,)
                )
                conn.commit()

            logger.info(f"Prescricao {prescricao_id} deleted successfully")

        except Exception as err:
            logger.error(f"Error deleting prescricao: {err}")
            raise DatabaseError(f"Failed to delete prescricao: {str(err)}")

    @staticmethod
    def _map_to_prescricao(data: dict) -> Prescricao:
        """
        Map database row to Prescricao model.

        Args:
            data: Database row as dictionary.

        Returns:
            Prescricao object.
        """
        return Prescricao(
            id=data.get("id"),
            consulta_id=data.get("consulta_id", 0),
            medicamento_id=data.get("medicamento_id", 0),
            duracao=data.get("duracao", ""),
            instrucoes=data.get("instrucoes", ""),
        )
