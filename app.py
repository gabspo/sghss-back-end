"""Main entry point for SGHSS Backend."""

import os
from src import create_app

if __name__ == "__main__":
    # Get environment
    env = os.getenv("FLASK_ENV", "development")

    # Create app
    app = create_app(env)

    # Get configuration from environment
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"

    # Run app
    app.run(host=host, port=port, debug=debug)
