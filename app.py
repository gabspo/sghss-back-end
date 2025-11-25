"""Main entry point for SGHSS Backend."""

import os
from src import create_app
from flasgger import Swagger

if __name__ == "__main__":
    # Get environment
    env = os.getenv("FLASK_ENV", "development")

    # Create app
    app = create_app(env)

    # Get configuration from environment
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"

    # Register Swagger UI (loads docs/openapi.yaml)
    try:
        Swagger(app, template_file='docs/openapi.yaml')
    except Exception:
        # If flasgger is not installed or template missing, continue without Swagger
        pass

    # Run app
    app.run(host=host, port=port, debug=debug)
