"""Usuario service for business logic."""

import logging
from typing import List, Optional

from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash

from ..config.database import get_db_manager
from ..exceptions import (
    AuthenticationError,
    ConflictError,
    DatabaseError,
    NotFoundError,
    ValidationError,
)
from ..models import Usuario
from ..utils.validators import Validator

logger = logging.getLogger(__name__)


class UsuarioService:
    """Service for usuario-related operations."""

    def __init__(self):
        """Initialize usuario service."""
        self.db_manager = get_db_manager()

    def criar_usuario(self, nome: str, email: str, senha: str, tipo: str) -> Usuario:
        """
        Create a new user.

        Args:
            nome: User name.
            email: User email.
            senha: User password.
            tipo: User type (admin, medico, paciente, etc).

        Returns:
            Created Usuario object.

        Raises:
            ValidationError: If validation fails.
            ConflictError: If email already exists.
            DatabaseError: If database operation fails.
        """
        # Validate inputs
        Validator.validate_required_fields(
            {"nome": nome, "email": email, "senha": senha, "tipo": tipo},
            ["nome", "email", "senha", "tipo"],
        )
        Validator.validate_email(email)
        Validator.validate_password_strength(senha)

        # Check if email already exists
        if self._email_exists(email):
            raise ConflictError("Email already registered")

        # Hash password
        senha_hash = generate_password_hash(senha)

        try:
            with self.db_manager.get_cursor() as (cursor, conn):
                cursor.execute(
                    """
                    INSERT INTO usuarios (nome, email, senha, tipo)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (nome, email, senha_hash, tipo),
                )
                conn.commit()
                usuario_id = cursor.lastrowid

            logger.info(f"Usuario created successfully: {usuario_id}")
            return self.obter_usuario_por_id(usuario_id)

        except Exception as err:
            logger.error(f"Error creating usuario: {err}")
            raise DatabaseError(f"Failed to create usuario: {str(err)}")

    def listar_usuarios(self, limite: int = 100, offset: int = 0) -> List[Usuario]:
        """
        List all users with pagination.

        Args:
            limite: Number of records to fetch.
            offset: Number of records to skip.

        Returns:
            List of Usuario objects.

        Raises:
            DatabaseError: If database operation fails.
        """
        try:
            with self.db_manager.get_cursor(dictionary=True) as (cursor, conn):
                cursor.execute(
                    """
                    SELECT id, nome, email, tipo FROM usuarios
                    LIMIT %s OFFSET %s
                    """,
                    (limite, offset),
                )
                usuarios_data = cursor.fetchall()

            usuarios = [self._map_to_usuario(data) for data in usuarios_data]
            logger.info(f"Listed {len(usuarios)} usuarios")
            return usuarios

        except Exception as err:
            logger.error(f"Error listing usuarios: {err}")
            raise DatabaseError(f"Failed to list usuarios: {str(err)}")

    def obter_usuario_por_id(self, usuario_id: int) -> Usuario:
        """
        Get user by ID.

        Args:
            usuario_id: User ID.

        Returns:
            Usuario object.

        Raises:
            NotFoundError: If user not found.
            DatabaseError: If database operation fails.
        """
        try:
            with self.db_manager.get_cursor(dictionary=True) as (cursor, conn):
                cursor.execute(
                    """
                    SELECT id, nome, email, tipo FROM usuarios
                    WHERE id = %s
                    """,
                    (usuario_id,),
                )
                usuario_data = cursor.fetchone()

            if not usuario_data:
                raise NotFoundError("Usuario not found")

            return self._map_to_usuario(usuario_data)

        except NotFoundError:
            raise
        except Exception as err:
            logger.error(f"Error getting usuario: {err}")
            raise DatabaseError(f"Failed to get usuario: {str(err)}")

    def obter_usuario_por_email(self, email: str) -> Usuario:
        """
        Get user by email.

        Args:
            email: User email.

        Returns:
            Usuario object.

        Raises:
            NotFoundError: If user not found.
            DatabaseError: If database operation fails.
        """
        try:
            with self.db_manager.get_cursor(dictionary=True) as (cursor, conn):
                cursor.execute(
                    """
                    SELECT id, nome, email, tipo, senha FROM usuarios
                    WHERE email = %s
                    """,
                    (email,),
                )
                usuario_data = cursor.fetchone()

            if not usuario_data:
                raise NotFoundError("Usuario not found")

            return self._map_to_usuario(usuario_data, include_password=True)

        except NotFoundError:
            raise
        except Exception as err:
            logger.error(f"Error getting usuario: {err}")
            raise DatabaseError(f"Failed to get usuario: {str(err)}")

    def atualizar_usuario(
        self, usuario_id: int, nome: str = None, email: str = None, tipo: str = None
    ) -> Usuario:
        """
        Update user.

        Args:
            usuario_id: User ID.
            nome: New name.
            email: New email.
            tipo: New type.

        Returns:
            Updated Usuario object.

        Raises:
            NotFoundError: If user not found.
            ValidationError: If validation fails.
            DatabaseError: If database operation fails.
        """
        # Check if user exists
        self.obter_usuario_por_id(usuario_id)

        # Validate email if provided
        if email:
            Validator.validate_email(email)
            if self._email_exists(email, exclude_id=usuario_id):
                raise ConflictError("Email already in use")

        try:
            updates = []
            params = []

            if nome is not None:
                updates.append("nome = %s")
                params.append(nome)
            if email is not None:
                updates.append("email = %s")
                params.append(email)
            if tipo is not None:
                updates.append("tipo = %s")
                params.append(tipo)

            if not updates:
                return self.obter_usuario_por_id(usuario_id)

            params.append(usuario_id)

            with self.db_manager.get_cursor() as (cursor, conn):
                cursor.execute(
                    f"""
                    UPDATE usuarios
                    SET {", ".join(updates)}
                    WHERE id = %s
                    """,
                    params,
                )
                conn.commit()

            logger.info(f"Usuario {usuario_id} updated successfully")
            return self.obter_usuario_por_id(usuario_id)

        except Exception as err:
            logger.error(f"Error updating usuario: {err}")
            raise DatabaseError(f"Failed to update usuario: {str(err)}")

    def deletar_usuario(self, usuario_id: int) -> None:
        """
        Delete user.

        Args:
            usuario_id: User ID.

        Raises:
            NotFoundError: If user not found.
            DatabaseError: If database operation fails.
        """
        # Check if user exists
        self.obter_usuario_por_id(usuario_id)

        try:
            with self.db_manager.get_cursor() as (cursor, conn):
                cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
                conn.commit()

            logger.info(f"Usuario {usuario_id} deleted successfully")

        except Exception as err:
            logger.error(f"Error deleting usuario: {err}")
            raise DatabaseError(f"Failed to delete usuario: {str(err)}")

    def autenticar(self, email: str, senha: str) -> tuple[Usuario, str]:
        """
        Authenticate user and return access token.

        Args:
            email: User email.
            senha: User password.

        Returns:
            Tuple of (Usuario object, access token).

        Raises:
            AuthenticationError: If credentials are invalid.
            DatabaseError: If database operation fails.
        """
        usuario = self.obter_usuario_por_email(email)

        if not check_password_hash(usuario.senha, senha):
            raise AuthenticationError("Invalid credentials")

        # Create JWT token
        access_token = create_access_token(identity=str(usuario.id))
        logger.info(f"User {usuario.id} authenticated successfully")

        return usuario, access_token

    def _email_exists(self, email: str, exclude_id: int = None) -> bool:
        """
        Check if email exists in database.

        Args:
            email: Email to check.
            exclude_id: User ID to exclude from check.

        Returns:
            True if email exists, False otherwise.
        """
        try:
            with self.db_manager.get_cursor(dictionary=True) as (cursor, conn):
                if exclude_id:
                    cursor.execute(
                        "SELECT id FROM usuarios WHERE email = %s AND id != %s",
                        (email, exclude_id),
                    )
                else:
                    cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
                return cursor.fetchone() is not None
        except Exception as err:
            logger.error(f"Error checking email: {err}")
            return False

    @staticmethod
    def _map_to_usuario(data: dict, include_password: bool = False) -> Usuario:
        """
        Map database row to Usuario model.

        Args:
            data: Database row as dictionary.
            include_password: Include password in model.

        Returns:
            Usuario object.
        """
        usuario = Usuario(
            id=data.get("id"),
            nome=data.get("nome", ""),
            email=data.get("email", ""),
            tipo=data.get("tipo", ""),
        )
        if include_password:
            usuario.senha = data.get("senha", "")
        return usuario
