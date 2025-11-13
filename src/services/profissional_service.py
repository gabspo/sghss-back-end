"""Profissional service for business logic."""

import logging
from typing import List

from ..config.database import get_db_manager
from ..exceptions import DatabaseError, NotFoundError, ValidationError
from ..models import Profissional
from ..utils.validators import Validator

logger = logging.getLogger(__name__)


class ProfissionalService:
    """Service for profissional-related operations."""

    def __init__(self):
        """Initialize profissional service."""
        self.db_manager = get_db_manager()

    def criar_profissional(
        self,
        nome: str,
        email: str,
        telefone: str,
        especialidade: str,
        registro: str,
    ) -> Profissional:
        """
        Create a new professional.

        Args:
            nome: Professional name.
            email: Professional email.
            telefone: Professional phone.
            especialidade: Medical specialty.
            registro: Medical registration number.

        Returns:
            Created Profissional object.

        Raises:
            ValidationError: If validation fails.
            DatabaseError: If database operation fails.
        """
        # Validate inputs
        Validator.validate_required_fields(
            {
                "nome": nome,
                "email": email,
                "telefone": telefone,
                "especialidade": especialidade,
                "registro": registro,
            },
            ["nome", "email", "telefone", "especialidade", "registro"],
        )
        Validator.validate_email(email)
        Validator.validate_phone(telefone)

        try:
            with self.db_manager.get_cursor() as (cursor, conn):
                cursor.execute(
                    """
                    INSERT INTO profissionais (nome, email, telefone, especialidade, registro)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (nome, email, telefone, especialidade, registro),
                )
                conn.commit()
                profissional_id = cursor.lastrowid

            logger.info(f"Profissional created successfully: {profissional_id}")
            return self.obter_profissional_por_id(profissional_id)

        except Exception as err:
            logger.error(f"Error creating profissional: {err}")
            raise DatabaseError(f"Failed to create profissional: {str(err)}")

    def listar_profissionais(
        self, limite: int = 100, offset: int = 0
    ) -> List[Profissional]:
        """
        List all professionals with pagination.

        Args:
            limite: Number of records to fetch.
            offset: Number of records to skip.

        Returns:
            List of Profissional objects.

        Raises:
            DatabaseError: If database operation fails.
        """
        try:
            with self.db_manager.get_cursor(dictionary=True) as (cursor, conn):
                cursor.execute(
                    """
                    SELECT id, nome, email, telefone, especialidade, registro
                    FROM profissionais
                    LIMIT %s OFFSET %s
                    """,
                    (limite, offset),
                )
                profissionais_data = cursor.fetchall()

            profissionais = [
                self._map_to_profissional(data) for data in profissionais_data
            ]
            logger.info(f"Listed {len(profissionais)} profissionais")
            return profissionais

        except Exception as err:
            logger.error(f"Error listing profissionais: {err}")
            raise DatabaseError(f"Failed to list profissionais: {str(err)}")

    def obter_profissional_por_id(self, profissional_id: int) -> Profissional:
        """
        Get professional by ID.

        Args:
            profissional_id: Professional ID.

        Returns:
            Profissional object.

        Raises:
            NotFoundError: If professional not found.
            DatabaseError: If database operation fails.
        """
        try:
            with self.db_manager.get_cursor(dictionary=True) as (cursor, conn):
                cursor.execute(
                    """
                    SELECT id, nome, email, telefone, especialidade, registro
                    FROM profissionais
                    WHERE id = %s
                    """,
                    (profissional_id,),
                )
                profissional_data = cursor.fetchone()

            if not profissional_data:
                raise NotFoundError("Profissional not found")

            return self._map_to_profissional(profissional_data)

        except NotFoundError:
            raise
        except Exception as err:
            logger.error(f"Error getting profissional: {err}")
            raise DatabaseError(f"Failed to get profissional: {str(err)}")

    def obter_profissional_por_registro(self, registro: str) -> Profissional:
        """
        Get professional by registration number.

        Args:
            registro: Medical registration number.

        Returns:
            Profissional object.

        Raises:
            NotFoundError: If professional not found.
            DatabaseError: If database operation fails.
        """
        try:
            with self.db_manager.get_cursor(dictionary=True) as (cursor, conn):
                cursor.execute(
                    """
                    SELECT id, nome, email, telefone, especialidade, registro
                    FROM profissionais
                    WHERE registro = %s
                    """,
                    (registro,),
                )
                profissional_data = cursor.fetchone()

            if not profissional_data:
                raise NotFoundError("Profissional not found")

            return self._map_to_profissional(profissional_data)

        except NotFoundError:
            raise
        except Exception as err:
            logger.error(f"Error getting profissional: {err}")
            raise DatabaseError(f"Failed to get profissional: {str(err)}")

    def atualizar_profissional(
        self,
        profissional_id: int,
        nome: str = None,
        email: str = None,
        telefone: str = None,
        especialidade: str = None,
    ) -> Profissional:
        """
        Update professional.

        Args:
            profissional_id: Professional ID.
            nome: New name.
            email: New email.
            telefone: New phone.
            especialidade: New specialty.

        Returns:
            Updated Profissional object.

        Raises:
            NotFoundError: If professional not found.
            ValidationError: If validation fails.
            DatabaseError: If database operation fails.
        """
        # Check if professional exists
        self.obter_profissional_por_id(profissional_id)

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
            if especialidade is not None:
                updates.append("especialidade = %s")
                params.append(especialidade)

            if not updates:
                return self.obter_profissional_por_id(profissional_id)

            params.append(profissional_id)

            with self.db_manager.get_cursor() as (cursor, conn):
                cursor.execute(
                    f"""
                    UPDATE profissionais
                    SET {", ".join(updates)}
                    WHERE id = %s
                    """,
                    params,
                )
                conn.commit()

            logger.info(f"Profissional {profissional_id} updated successfully")
            return self.obter_profissional_por_id(profissional_id)

        except Exception as err:
            logger.error(f"Error updating profissional: {err}")
            raise DatabaseError(f"Failed to update profissional: {str(err)}")

    def deletar_profissional(self, profissional_id: int) -> None:
        """
        Delete professional.

        Args:
            profissional_id: Professional ID.

        Raises:
            NotFoundError: If professional not found.
            DatabaseError: If database operation fails.
        """
        # Check if professional exists
        self.obter_profissional_por_id(profissional_id)

        try:
            with self.db_manager.get_cursor() as (cursor, conn):
                cursor.execute(
                    "DELETE FROM profissionais WHERE id = %s", (profissional_id,)
                )
                conn.commit()

            logger.info(f"Profissional {profissional_id} deleted successfully")

        except Exception as err:
            logger.error(f"Error deleting profissional: {err}")
            raise DatabaseError(f"Failed to delete profissional: {str(err)}")

    @staticmethod
    def _map_to_profissional(data: dict) -> Profissional:
        """
        Map database row to Profissional model.

        Args:
            data: Database row as dictionary.

        Returns:
            Profissional object.
        """
        return Profissional(
            id=data.get("id"),
            nome=data.get("nome", ""),
            email=data.get("email", ""),
            telefone=data.get("telefone", ""),
            especialidade=data.get("especialidade", ""),
            registro=data.get("registro", ""),
        )
