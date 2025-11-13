"""Paciente service for business logic."""

import logging
from typing import List

from ..config.database import get_db_manager
from ..exceptions import DatabaseError, NotFoundError, ValidationError
from ..models import Paciente
from ..utils.validators import Validator

logger = logging.getLogger(__name__)


class PacienteService:
    """Service for paciente-related operations."""

    def __init__(self):
        """Initialize paciente service."""
        self.db_manager = get_db_manager()

    def criar_paciente(
        self,
        nome: str,
        email: str,
        telefone: str,
        cpf: str,
        data_nascimento: str = None,
        endereco: str = None,
    ) -> Paciente:
        """
        Create a new patient.

        Args:
            nome: Patient name.
            email: Patient email.
            telefone: Patient phone.
            cpf: Patient CPF.
            data_nascimento: Birth date.
            endereco: Address.

        Returns:
            Created Paciente object.

        Raises:
            ValidationError: If validation fails.
            DatabaseError: If database operation fails.
        """
        # Validate inputs
        Validator.validate_required_fields(
            {"nome": nome, "email": email, "telefone": telefone, "cpf": cpf},
            ["nome", "email", "telefone", "cpf"],
        )
        Validator.validate_email(email)
        Validator.validate_phone(telefone)

        try:
            with self.db_manager.get_cursor() as (cursor, conn):
                cursor.execute(
                    """
                    INSERT INTO pacientes (nome, email, telefone, cpf, data_nascimento, endereco)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (nome, email, telefone, cpf, data_nascimento, endereco),
                )
                conn.commit()
                paciente_id = cursor.lastrowid

            logger.info(f"Paciente created successfully: {paciente_id}")
            return self.obter_paciente_por_id(paciente_id)

        except Exception as err:
            logger.error(f"Error creating paciente: {err}")
            raise DatabaseError(f"Failed to create paciente: {str(err)}")

    def listar_pacientes(self, limite: int = 100, offset: int = 0) -> List[Paciente]:
        """
        List all patients with pagination.

        Args:
            limite: Number of records to fetch.
            offset: Number of records to skip.

        Returns:
            List of Paciente objects.

        Raises:
            DatabaseError: If database operation fails.
        """
        try:
            with self.db_manager.get_cursor(dictionary=True) as (cursor, conn):
                cursor.execute(
                    """
                    SELECT id, nome, email, telefone, cpf, data_nascimento, endereco
                    FROM pacientes
                    LIMIT %s OFFSET %s
                    """,
                    (limite, offset),
                )
                pacientes_data = cursor.fetchall()

            pacientes = [self._map_to_paciente(data) for data in pacientes_data]
            logger.info(f"Listed {len(pacientes)} pacientes")
            return pacientes

        except Exception as err:
            logger.error(f"Error listing pacientes: {err}")
            raise DatabaseError(f"Failed to list pacientes: {str(err)}")

    def obter_paciente_por_id(self, paciente_id: int) -> Paciente:
        """
        Get patient by ID.

        Args:
            paciente_id: Patient ID.

        Returns:
            Paciente object.

        Raises:
            NotFoundError: If patient not found.
            DatabaseError: If database operation fails.
        """
        try:
            with self.db_manager.get_cursor(dictionary=True) as (cursor, conn):
                cursor.execute(
                    """
                    SELECT id, nome, email, telefone, cpf, data_nascimento, endereco
                    FROM pacientes
                    WHERE id = %s
                    """,
                    (paciente_id,),
                )
                paciente_data = cursor.fetchone()

            if not paciente_data:
                raise NotFoundError("Paciente not found")

            return self._map_to_paciente(paciente_data)

        except NotFoundError:
            raise
        except Exception as err:
            logger.error(f"Error getting paciente: {err}")
            raise DatabaseError(f"Failed to get paciente: {str(err)}")

    def atualizar_paciente(
        self,
        paciente_id: int,
        nome: str = None,
        email: str = None,
        telefone: str = None,
        endereco: str = None,
    ) -> Paciente:
        """
        Update patient.

        Args:
            paciente_id: Patient ID.
            nome: New name.
            email: New email.
            telefone: New phone.
            endereco: New address.

        Returns:
            Updated Paciente object.

        Raises:
            NotFoundError: If patient not found.
            ValidationError: If validation fails.
            DatabaseError: If database operation fails.
        """
        # Check if patient exists
        self.obter_paciente_por_id(paciente_id)

        # Validate inputs if provided
        if email:
            Validator.validate_email(email)
        if telefone:
            Validator.validate_phone(telefone)

        try:
            updates = []
            params = []

            if nome is not None:
                updates.append("nome = %s")
                params.append(nome)
            if email is not None:
                updates.append("email = %s")
                params.append(email)
            if telefone is not None:
                updates.append("telefone = %s")
                params.append(telefone)
            if endereco is not None:
                updates.append("endereco = %s")
                params.append(endereco)

            if not updates:
                return self.obter_paciente_por_id(paciente_id)

            params.append(paciente_id)

            with self.db_manager.get_cursor() as (cursor, conn):
                cursor.execute(
                    f"""
                    UPDATE pacientes
                    SET {", ".join(updates)}
                    WHERE id = %s
                    """,
                    params,
                )
                conn.commit()

            logger.info(f"Paciente {paciente_id} updated successfully")
            return self.obter_paciente_por_id(paciente_id)

        except Exception as err:
            logger.error(f"Error updating paciente: {err}")
            raise DatabaseError(f"Failed to update paciente: {str(err)}")

    def deletar_paciente(self, paciente_id: int) -> None:
        """
        Delete patient.

        Args:
            paciente_id: Patient ID.

        Raises:
            NotFoundError: If patient not found.
            DatabaseError: If database operation fails.
        """
        # Check if patient exists
        self.obter_paciente_por_id(paciente_id)

        try:
            with self.db_manager.get_cursor() as (cursor, conn):
                cursor.execute("DELETE FROM pacientes WHERE id = %s", (paciente_id,))
                conn.commit()

            logger.info(f"Paciente {paciente_id} deleted successfully")

        except Exception as err:
            logger.error(f"Error deleting paciente: {err}")
            raise DatabaseError(f"Failed to delete paciente: {str(err)}")

    @staticmethod
    def _map_to_paciente(data: dict) -> Paciente:
        """
        Map database row to Paciente model.

        Args:
            data: Database row as dictionary.

        Returns:
            Paciente object.
        """
        return Paciente(
            id=data.get("id"),
            nome=data.get("nome", ""),
            email=data.get("email", ""),
            telefone=data.get("telefone", ""),
            cpf=data.get("cpf", ""),
            data_nascimento=data.get("data_nascimento"),
            endereco=data.get("endereco", ""),
        )
