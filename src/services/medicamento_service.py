"""Medicamento service for business logic."""

import logging
from typing import List

from ..config.database import get_db_manager
from ..exceptions import DatabaseError, NotFoundError, ValidationError
from ..models import Medicamento
from ..utils.validators import Validator

logger = logging.getLogger(__name__)


class MedicamentoService:
    """Service for medicamento-related operations."""

    def __init__(self):
        """Initialize medicamento service."""
        self.db_manager = get_db_manager()

    def criar_medicamento(
        self,
        nome: str,
        descricao: str = None,
        dosagem: str = None,
    ) -> Medicamento:
        """
        Create a new medication.

        Args:
            nome: Medication name.
            descricao: Medication description.
            dosagem: Dosage information.

        Returns:
            Created Medicamento object.

        Raises:
            ValidationError: If validation fails.
            DatabaseError: If database operation fails.
        """
        # Validate inputs
        Validator.validate_required_fields(
            {"nome": nome},
            ["nome"],
        )

        try:
            with self.db_manager.get_cursor() as (cursor, conn):
                cursor.execute(
                    """
                    INSERT INTO medicamentos (nome, descricao, dosagem)
                    VALUES (%s, %s, %s)
                    """,
                    (nome, descricao, dosagem),
                )
                conn.commit()
                medicamento_id = cursor.lastrowid

            logger.info(f"Medicamento created successfully: {medicamento_id}")
            return self.obter_medicamento_por_id(medicamento_id)

        except Exception as err:
            logger.error(f"Error creating medicamento: {err}")
            raise DatabaseError(f"Failed to create medicamento: {str(err)}")

    def listar_medicamentos(self, limite: int = 100, offset: int = 0) -> List[Medicamento]:
        """
        List all medications with pagination.

        Args:
            limite: Number of records to fetch.
            offset: Number of records to skip.

        Returns:
            List of Medicamento objects.

        Raises:
            DatabaseError: If database operation fails.
        """
        try:
            with self.db_manager.get_cursor(dictionary=True) as (cursor, conn):
                cursor.execute(
                    """
                    SELECT id, nome, descricao, dosagem
                    FROM medicamentos
                    ORDER BY nome
                    LIMIT %s OFFSET %s
                    """,
                    (limite, offset),
                )
                medicamentos_data = cursor.fetchall()

            medicamentos = [
                self._map_to_medicamento(data) for data in medicamentos_data
            ]
            logger.info(f"Listed {len(medicamentos)} medicamentos")
            return medicamentos

        except Exception as err:
            logger.error(f"Error listing medicamentos: {err}")
            raise DatabaseError(f"Failed to list medicamentos: {str(err)}")

    def obter_medicamento_por_id(self, medicamento_id: int) -> Medicamento:
        """
        Get medication by ID.

        Args:
            medicamento_id: Medication ID.

        Returns:
            Medicamento object.

        Raises:
            NotFoundError: If medication not found.
            DatabaseError: If database operation fails.
        """
        try:
            with self.db_manager.get_cursor(dictionary=True) as (cursor, conn):
                cursor.execute(
                    """
                    SELECT id, nome, descricao, dosagem
                    FROM medicamentos
                    WHERE id = %s
                    """,
                    (medicamento_id,),
                )
                medicamento_data = cursor.fetchone()

            if not medicamento_data:
                raise NotFoundError("Medicamento not found")

            return self._map_to_medicamento(medicamento_data)

        except NotFoundError:
            raise
        except Exception as err:
            logger.error(f"Error getting medicamento: {err}")
            raise DatabaseError(f"Failed to get medicamento: {str(err)}")

    def buscar_medicamentos_por_nome(
        self, nome: str, limite: int = 100, offset: int = 0
    ) -> List[Medicamento]:
        """
        Search medications by name.

        Args:
            nome: Medication name to search.
            limite: Number of records to fetch.
            offset: Number of records to skip.

        Returns:
            List of Medicamento objects.

        Raises:
            DatabaseError: If database operation fails.
        """
        try:
            with self.db_manager.get_cursor(dictionary=True) as (cursor, conn):
                cursor.execute(
                    """
                    SELECT id, nome, descricao, dosagem
                    FROM medicamentos
                    WHERE nome LIKE %s
                    ORDER BY nome
                    LIMIT %s OFFSET %s
                    """,
                    (f"%{nome}%", limite, offset),
                )
                medicamentos_data = cursor.fetchall()

            medicamentos = [
                self._map_to_medicamento(data) for data in medicamentos_data
            ]
            logger.info(f"Found {len(medicamentos)} medicamentos matching '{nome}'")
            return medicamentos

        except Exception as err:
            logger.error(f"Error searching medicamentos: {err}")
            raise DatabaseError(f"Failed to search medicamentos: {str(err)}")

    def atualizar_medicamento(
        self,
        medicamento_id: int,
        nome: str = None,
        descricao: str = None,
        dosagem: str = None,
    ) -> Medicamento:
        """
        Update medication.

        Args:
            medicamento_id: Medication ID.
            nome: New name.
            descricao: New description.
            dosagem: New dosage.

        Returns:
            Updated Medicamento object.

        Raises:
            NotFoundError: If medication not found.
            DatabaseError: If database operation fails.
        """
        # Check if medication exists
        self.obter_medicamento_por_id(medicamento_id)

        try:
            updates = []
            params = []

            if nome is not None:
                updates.append("nome = %s")
                params.append(nome)
            if descricao is not None:
                updates.append("descricao = %s")
                params.append(descricao)
            if dosagem is not None:
                updates.append("dosagem = %s")
                params.append(dosagem)

            if not updates:
                return self.obter_medicamento_por_id(medicamento_id)

            params.append(medicamento_id)

            with self.db_manager.get_cursor() as (cursor, conn):
                cursor.execute(
                    f"""
                    UPDATE medicamentos
                    SET {", ".join(updates)}
                    WHERE id = %s
                    """,
                    params,
                )
                conn.commit()

            logger.info(f"Medicamento {medicamento_id} updated successfully")
            return self.obter_medicamento_por_id(medicamento_id)

        except Exception as err:
            logger.error(f"Error updating medicamento: {err}")
            raise DatabaseError(f"Failed to update medicamento: {str(err)}")

    def deletar_medicamento(self, medicamento_id: int) -> None:
        """
        Delete medication.

        Args:
            medicamento_id: Medication ID.

        Raises:
            NotFoundError: If medication not found.
            DatabaseError: If database operation fails.
        """
        # Check if medication exists
        self.obter_medicamento_por_id(medicamento_id)

        try:
            with self.db_manager.get_cursor() as (cursor, conn):
                cursor.execute(
                    "DELETE FROM medicamentos WHERE id = %s", (medicamento_id,)
                )
                conn.commit()

            logger.info(f"Medicamento {medicamento_id} deleted successfully")

        except Exception as err:
            logger.error(f"Error deleting medicamento: {err}")
            raise DatabaseError(f"Failed to delete medicamento: {str(err)}")

    @staticmethod
    def _map_to_medicamento(data: dict) -> Medicamento:
        """
        Map database row to Medicamento model.

        Args:
            data: Database row as dictionary.

        Returns:
            Medicamento object.
        """
        return Medicamento(
            id=data.get("id"),
            nome=data.get("nome", ""),
            descricao=data.get("descricao", ""),
            dosagem=data.get("dosagem", ""),
        )
