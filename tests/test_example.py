"""Example tests for SGHSS application."""

import pytest
from unittest.mock import Mock, patch, MagicMock

# Exemplo de testes unitários


class TestValidator:
    """Tests for Validator utility class."""

    def test_validate_email_valid(self):
        """Test email validation with valid email."""
        from src.utils.validators import Validator
        from src.exceptions import ValidationError

        # Should not raise
        try:
            Validator.validate_email("user@example.com")
        except ValidationError:
            pytest.fail("validate_email raised ValidationError unexpectedly")

    def test_validate_email_invalid(self):
        """Test email validation with invalid email."""
        from src.utils.validators import Validator
        from src.exceptions import ValidationError

        with pytest.raises(ValidationError):
            Validator.validate_email("invalid-email")

    def test_validate_password_strength_valid(self):
        """Test password validation with valid password."""
        from src.utils.validators import Validator
        from src.exceptions import ValidationError

        # Should not raise
        try:
            Validator.validate_password_strength("SecurePass123")
        except ValidationError:
            pytest.fail("validate_password_strength raised ValidationError unexpectedly")

    def test_validate_password_strength_too_short(self):
        """Test password validation with too short password."""
        from src.utils.validators import Validator
        from src.exceptions import ValidationError

        with pytest.raises(ValidationError):
            Validator.validate_password_strength("weak", min_length=10)


class TestUsuarioService:
    """Tests for UsuarioService."""

    @pytest.fixture
    def mock_db_manager(self):
        """Mock database manager."""
        return MagicMock()

    @pytest.fixture
    def usuario_service(self, mock_db_manager):
        """Create UsuarioService with mocked database."""
        from src.services.usuario_service import UsuarioService

        service = UsuarioService()
        service.db_manager = mock_db_manager
        return service

    def test_criar_usuario_success(self, usuario_service):
        """Test successful user creation."""
        from src.models import Usuario

        # Mock the database cursor
        mock_cursor = MagicMock()
        mock_cursor.lastrowid = 1
        mock_conn = MagicMock()

        usuario_service.db_manager.get_cursor.return_value.__enter__.return_value = (
            mock_cursor,
            mock_conn,
        )

        # Mock the usuario fetch
        usuario_service.obter_usuario_por_id = MagicMock(
            return_value=Usuario(
                id=1,
                nome="John Doe",
                email="john@example.com",
                tipo="patient",
            )
        )

        # Create user
        usuario = usuario_service.criar_usuario(
            nome="John Doe",
            email="john@example.com",
            senha="secure_password_123",
            tipo="patient",
        )

        # Assertions
        assert usuario.id == 1
        assert usuario.nome == "John Doe"
        assert usuario.email == "john@example.com"

    def test_criar_usuario_invalid_email(self, usuario_service):
        """Test user creation with invalid email."""
        from src.exceptions import ValidationError

        with pytest.raises(ValidationError):
            usuario_service.criar_usuario(
                nome="John Doe",
                email="invalid-email",
                senha="secure_password_123",
                tipo="patient",
            )


class TestResponseFormatter:
    """Tests for ResponseFormatter utility."""

    def test_success_response(self):
        """Test successful response formatting."""
        from src.utils.response import ResponseFormatter

        response, status_code = ResponseFormatter.success(
            data={"id": 1, "name": "Test"},
            message="Success",
            status_code=200,
        )

        assert status_code == 200
        # Check response structure
        json_data = response.get_json()
        assert json_data["status"] == "success"
        assert json_data["message"] == "Success"
        assert json_data["data"]["id"] == 1

    def test_error_response(self):
        """Test error response formatting."""
        from src.utils.response import ResponseFormatter

        response, status_code = ResponseFormatter.error(
            message="Not found",
            error_code="NOT_FOUND",
            status_code=404,
        )

        assert status_code == 404
        json_data = response.get_json()
        assert json_data["status"] == "error"
        assert json_data["error_code"] == "NOT_FOUND"

    def test_paginated_response(self):
        """Test paginated response formatting."""
        from src.utils.response import ResponseFormatter

        response, status_code = ResponseFormatter.paginated(
            data=[{"id": 1}, {"id": 2}],
            total=100,
            page=1,
            per_page=2,
        )

        json_data = response.get_json()
        assert json_data["pagination"]["page"] == 1
        assert json_data["pagination"]["per_page"] == 2
        assert json_data["pagination"]["total"] == 100
        assert json_data["pagination"]["total_pages"] == 50


if __name__ == "__main__":
    pytest.main([__file__])
