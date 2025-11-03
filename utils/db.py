"""
Database Connection Utilities
Centralized database connection management
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config


def get_db_connection():
    """
    Establish and return a database connection with RealDictCursor

    Returns:
        psycopg2.connection: Database connection object with dict cursor

    Raises:
        Exception: If connection fails

    Example:
        >>> conn = get_db_connection()
        >>> cursor = conn.cursor()
        >>> cursor.execute("SELECT * FROM users")
        >>> results = cursor.fetchall()  # Returns list of dicts
    """
    try:
        conn = psycopg2.connect(Config.DATABASE_URL, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        raise Exception(f"Database connection failed: {str(e)}")


def test_connection():
    """
    Test database connection and return version info

    Returns:
        dict: Database connection information

    Example:
        >>> info = test_connection()
        >>> print(info['connected'])
        True
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT version();")
        version = cursor.fetchone()['version']

        cursor.execute("SELECT current_database();")
        db_name = cursor.fetchone()['current_database']

        cursor.close()
        conn.close()

        return {
            'connected': True,
            'database': db_name,
            'version': version.split(',')[0]
        }
    except Exception as e:
        return {
            'connected': False,
            'error': str(e)
        }
