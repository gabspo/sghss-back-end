"""Database connection manager."""

import logging
from contextlib import contextmanager
from typing import Generator

import mysql.connector
from mysql.connector import MySQLConnection, Error as MySQLError

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections and operations."""

    def __init__(self, config: dict):
        """
        Initialize the database manager.

        Args:
            config: Database configuration dictionary.
        """
        self.config = config
        self.connection = None

    def connect(self) -> MySQLConnection:
        """
        Establish a database connection.

        Returns:
            MySQLConnection: The database connection.

        Raises:
            MySQLError: If connection fails.
        """
        try:
            self.connection = mysql.connector.connect(**self.config)
            logger.info("Database connection established successfully")
            return self.connection
        except MySQLError as err:
            logger.error(f"Database connection failed: {err}")
            raise

    def disconnect(self):
        """Close the database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Database connection closed")

    @contextmanager
    def get_connection(self) -> Generator[MySQLConnection, None, None]:
        """
        Context manager for database connections.

        Yields:
            MySQLConnection: A database connection.
        """
        try:
            conn = mysql.connector.connect(**self.config)
            yield conn
        except MySQLError as err:
            logger.error(f"Database error: {err}")
            raise
        finally:
            if conn and conn.is_connected():
                conn.close()

    @contextmanager
    def get_cursor(self, dictionary: bool = False) -> Generator:
        """
        Context manager for database cursors.

        Args:
            dictionary: If True, return results as dictionaries.

        Yields:
            Cursor: A database cursor.
        """
        with self.get_connection() as conn:
            try:
                cursor = conn.cursor(dictionary=dictionary)
                yield cursor, conn
            finally:
                if cursor:
                    cursor.close()


# Global database manager instance
_db_manager = None


def initialize_db(config: dict) -> DatabaseManager:
    """
    Initialize the global database manager.

    Args:
        config: Database configuration dictionary.

    Returns:
        DatabaseManager: The initialized database manager.
    """
    global _db_manager
    _db_manager = DatabaseManager(config)
    return _db_manager


def get_db_manager() -> DatabaseManager:
    """
    Get the global database manager.

    Returns:
        DatabaseManager: The database manager instance.
    """
    if _db_manager is None:
        raise RuntimeError("Database manager not initialized")
    return _db_manager
