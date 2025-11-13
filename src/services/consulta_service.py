"""Consulta service for business logic."""

import logging
from typing import List, Optional
from datetime import datetime

from ..config.database import get_db_manager
from ..exceptions import DatabaseError, NotFoundError, ValidationError
from ..models import Consulta
from ..utils.validators import Validator

logger = logging.getLogger(__name__)


class ConsultaService:
    """Service for consulta-related operations."""

    def __init__(self):
        """Initialize consulta service."""
        self.db_manager = get_db_manager()

    def criar_consulta(
        self,
        paciente_id: int,
        data: str,
        motivo: str,
        observacoes: str = None,
        profissional_id: int = None,
        tipo_consulta: str = "presencial",
        link_video: str = None,
    ) -> Consulta:
        """
        Create a new consultation.

        Args:
            paciente_id: Patient ID.
            data: Consultation date and time (ISO format).
            motivo: Reason for consultation.
            observacoes: Additional observations.
            profissional_id: Professional ID.
            tipo_consulta: Type (presencial or telemedicina).
            link_video: Video call link for telemedicine.

        Returns:
            Created Consulta object.

        Raises:
            ValidationError: If validation fails.
            DatabaseError: If database operation fails.
        """
        # Validate inputs
        Validator.validate_required_fields(
            {
                "paciente_id": paciente_id,
                "data": data,
                "motivo": motivo,
            },
            ["paciente_id", "data", "motivo"],
        )
        Validator.validate_date_format(data, "%Y-%m-%d %H:%M:%S")

        # Validate telemedicina has link
        if tipo_consulta == "telemedicina" and not link_video:
            raise ValidationError("Video link is required for telemedicina")

        try:
            with self.db_manager.get_cursor() as (cursor, conn):
                cursor.execute(
                    """
                    INSERT INTO consultas 
                    (paciente_id, profissional_id, data, motivo, observacoes, tipo_consulta, link_video)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        paciente_id,
                        profissional_id,
                        data,
                        motivo,
                        observacoes,
                        tipo_consulta,
                        link_video,
                    ),
                )
                conn.commit()
                consulta_id = cursor.lastrowid

            logger.info(f"Consulta created successfully: {consulta_id}")
            return self.obter_consulta_por_id(consulta_id)

        except Exception as err:
            logger.error(f"Error creating consulta: {err}")
            raise DatabaseError(f"Failed to create consulta: {str(err)}")

    def listar_consultas(
        self, limite: int = 100, offset: int = 0, paciente_id: int = None
    ) -> List[Consulta]:
        """
        List all consultations with pagination and optional filtering.

        Args:
            limite: Number of records to fetch.
            offset: Number of records to skip.
            paciente_id: Filter by patient ID.

        Returns:
            List of Consulta objects.

        Raises:
            DatabaseError: If database operation fails.
        """
        try:
            if paciente_id:
                query = """
                    SELECT id, paciente_id, profissional_id, data, motivo, observacoes,
                           tipo_consulta, link_video
                    FROM consultas
                    WHERE paciente_id = %s
                    ORDER BY data DESC
                    LIMIT %s OFFSET %s
                """
                params = (paciente_id, limite, offset)
            else:
                query = """
                    SELECT id, paciente_id, profissional_id, data, motivo, observacoes,
                           tipo_consulta, link_video
                    FROM consultas
                    ORDER BY data DESC
                    LIMIT %s OFFSET %s
                """
                params = (limite, offset)

            with self.db_manager.get_cursor(dictionary=True) as (cursor, conn):
                cursor.execute(query, params)
                consultas_data = cursor.fetchall()

            consultas = [self._map_to_consulta(data) for data in consultas_data]
            logger.info(f"Listed {len(consultas)} consultas")
            return consultas

        except Exception as err:
            logger.error(f"Error listing consultas: {err}")
            raise DatabaseError(f"Failed to list consultas: {str(err)}")

    def obter_consulta_por_id(self, consulta_id: int) -> Consulta:
        """
        Get consultation by ID.

        Args:
            consulta_id: Consultation ID.

        Returns:
            Consulta object.

        Raises:
            NotFoundError: If consultation not found.
            DatabaseError: If database operation fails.
        """
        try:
            with self.db_manager.get_cursor(dictionary=True) as (cursor, conn):
                cursor.execute(
                    """
                    SELECT id, paciente_id, profissional_id, data, motivo, observacoes,
                           tipo_consulta, link_video
                    FROM consultas
                    WHERE id = %s
                    """,
                    (consulta_id,),
                )
                consulta_data = cursor.fetchone()

            if not consulta_data:
                raise NotFoundError("Consulta not found")

            return self._map_to_consulta(consulta_data)

        except NotFoundError:
            raise
        except Exception as err:
            logger.error(f"Error getting consulta: {err}")
            raise DatabaseError(f"Failed to get consulta: {str(err)}")

    def atualizar_consulta(
        self,
        consulta_id: int,
        data: str = None,
        motivo: str = None,
        observacoes: str = None,
        link_video: str = None,
    ) -> Consulta:
        """
        Update consultation.

        Args:
            consulta_id: Consultation ID.
            data: New date and time.
            motivo: New reason.
            observacoes: New observations.
            link_video: New video link.

        Returns:
            Updated Consulta object.

        Raises:
            NotFoundError: If consultation not found.
            ValidationError: If validation fails.
            DatabaseError: If database operation fails.
        """
        # Check if consultation exists
        consulta = self.obter_consulta_por_id(consulta_id)

        # Validate date if provided
        if data:
            Validator.validate_date_format(data, "%Y-%m-%d %H:%M:%S")

        try:
            updates = []
            params = []

            if data is not None:
                updates.append("data = %s")
                params.append(data)
            if motivo is not None:
                updates.append("motivo = %s")
                params.append(motivo)
            if observacoes is not None:
                updates.append("observacoes = %s")
                params.append(observacoes)
            if link_video is not None:
                updates.append("link_video = %s")
                params.append(link_video)

            if not updates:
                return self.obter_consulta_por_id(consulta_id)

            params.append(consulta_id)

            with self.db_manager.get_cursor() as (cursor, conn):
                cursor.execute(
                    f"""
                    UPDATE consultas
                    SET {", ".join(updates)}
                    WHERE id = %s
                    """,
                    params,
                )
                conn.commit()

            logger.info(f"Consulta {consulta_id} updated successfully")
            return self.obter_consulta_por_id(consulta_id)

        except Exception as err:
            logger.error(f"Error updating consulta: {err}")
            raise DatabaseError(f"Failed to update consulta: {str(err)}")

    def deletar_consulta(self, consulta_id: int) -> None:
        """
        Delete consultation.

        Args:
            consulta_id: Consultation ID.

        Raises:
            NotFoundError: If consultation not found.
            DatabaseError: If database operation fails.
        """
        # Check if consultation exists
        self.obter_consulta_por_id(consulta_id)

        try:
            with self.db_manager.get_cursor() as (cursor, conn):
                cursor.execute("DELETE FROM consultas WHERE id = %s", (consulta_id,))
                conn.commit()

            logger.info(f"Consulta {consulta_id} deleted successfully")

        except Exception as err:
            logger.error(f"Error deleting consulta: {err}")
            raise DatabaseError(f"Failed to delete consulta: {str(err)}")

    def listar_consultas_por_paciente(
        self, paciente_id: int, limite: int = 100, offset: int = 0
    ) -> List[Consulta]:
        """
        List consultations for a specific patient.

        Args:
            paciente_id: Patient ID.
            limite: Number of records to fetch.
            offset: Number of records to skip.

        Returns:
            List of Consulta objects.

        Raises:
            DatabaseError: If database operation fails.
        """
        return self.listar_consultas(
            limite=limite, offset=offset, paciente_id=paciente_id
        )

    @staticmethod
    def _map_to_consulta(data: dict) -> Consulta:
        """
        Map database row to Consulta model.

        Args:
            data: Database row as dictionary.

        Returns:
            Consulta object.
        """
        return Consulta(
            id=data.get("id"),
            paciente_id=data.get("paciente_id", 0),
            profissional_id=data.get("profissional_id"),
            data=data.get("data", ""),
            motivo=data.get("motivo", ""),
            observacoes=data.get("observacoes", ""),
            tipo_consulta=data.get("tipo_consulta", "presencial"),
            link_video=data.get("link_video"),
        )
