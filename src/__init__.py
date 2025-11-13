"""SGHSS Backend Application Entry Point."""

import logging
import os
from flask import Flask
from flask_jwt_extended import JWTManager

from .config import get_config
from .config.database import initialize_db
from .utils.logging import setup_logging
from .exceptions import SGHSSException
from .utils.response import ResponseFormatter
from .routes.auth import auth_bp
from .routes.usuarios import usuario_bp
from .routes.pacientes import paciente_bp
from .routes.profissionais import profissional_bp
from .routes.consultas import consulta_bp
from .routes.medicamentos import medicamento_bp
from .routes.prescricoes import prescricao_bp

# Setup logging
setup_logging(log_level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def create_app(config_env: str = None) -> Flask:
    """
    Create and configure the Flask application.

    Args:
        config_env: Environment name (development, production, testing).

    Returns:
        Configured Flask application instance.
    """
    # Get configuration
    config = get_config(config_env)

    # Create Flask app
    app = Flask(__name__)
    app.config.from_object(config)

    # Initialize database
    initialize_db(config.DB_CONFIG)
    logger.info("Database initialized")

    # Initialize JWT
    jwt = JWTManager(app)
    logger.info("JWT initialized")

    # Register error handlers
    register_error_handlers(app)

    # Register blueprints
    register_blueprints(app)

    # Register CLI commands
    register_cli_commands(app)

    logger.info("Application created successfully")
    return app


def register_error_handlers(app: Flask) -> None:
    """
    Register global error handlers.

    Args:
        app: Flask application instance.
    """

    @app.errorhandler(SGHSSException)
    def handle_sghss_exception(error: SGHSSException):
        """Handle SGHSS custom exceptions."""
        return ResponseFormatter.error(
            message=error.message,
            error_code="SGHSS_ERROR",
            status_code=error.status_code,
        )

    @app.errorhandler(404)
    def handle_not_found(error):
        """Handle 404 errors."""
        return ResponseFormatter.error(
            message="Resource not found",
            error_code="NOT_FOUND",
            status_code=404,
        )

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        """Handle 405 errors."""
        return ResponseFormatter.error(
            message="Method not allowed",
            error_code="METHOD_NOT_ALLOWED",
            status_code=405,
        )

    @app.errorhandler(500)
    def handle_internal_error(error):
        """Handle 500 errors."""
        logger.error(f"Internal server error: {error}")
        return ResponseFormatter.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500,
        )


def register_blueprints(app: Flask) -> None:
    """
    Register Flask blueprints.

    Args:
        app: Flask application instance.
    """
    app.register_blueprint(auth_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(paciente_bp)
    app.register_blueprint(profissional_bp)
    app.register_blueprint(consulta_bp)
    app.register_blueprint(medicamento_bp)
    app.register_blueprint(prescricao_bp)
    logger.info("Blueprints registered")


def register_cli_commands(app: Flask) -> None:
    """
    Register Flask CLI commands.

    Args:
        app: Flask application instance.
    """

    @app.cli.command()
    def init_db():
        """Initialize database tables."""
        logger.info("Initializing database...")
        # TODO: Implement database initialization script
        logger.info("Database initialized")


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
