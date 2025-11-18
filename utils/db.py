"""
Database Connection Utilities
Centralized database connection management with pooling and retry logic
"""

import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from config import Config
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global connection pool
connection_pool = None

def initialize_connection_pool():
    """Initialize the connection pool"""
    global connection_pool
    try:
        connection_pool = psycopg2.pool.SimpleConnectionPool(
            1,  # min connections
            20,  # max connections (increased from 10 to prevent exhaustion)
            Config.DATABASE_URL,
            cursor_factory=RealDictCursor,
            connect_timeout=10
        )
        if connection_pool:
            logger.info("✅ Connection pool created successfully (size: 1-20)")
    except Exception as e:
        logger.error(f"❌ Error creating connection pool: {e}")
        connection_pool = None

# Initialize pool on module load
initialize_connection_pool()


def get_db_connection(retries=3, delay=2):
    """
    Establish and return a database connection with retry logic

    Args:
        retries (int): Number of retry attempts (default: 3)
        delay (int): Base delay between retries in seconds (default: 2)

    Returns:
        psycopg2.connection: Database connection object with dict cursor

    Raises:
        Exception: If connection fails after all retries

    Example:
        >>> conn = get_db_connection(retries=3, delay=2)
        >>> cursor = conn.cursor()
        >>> cursor.execute("SELECT * FROM users")
        >>> results = cursor.fetchall()  # Returns list of dicts
    """
    global connection_pool

    for attempt in range(retries):
        try:
            # Try to get connection from pool
            if connection_pool:
                conn = connection_pool.getconn()
                if conn:
                    # Set statement timeout to prevent long-running queries
                    try:
                        cur = conn.cursor()
                        cur.execute("SET statement_timeout = 30000")  # 30 seconds
                        cur.close()
                    except Exception as timeout_error:
                        logger.warning(f"Could not set statement timeout: {timeout_error}")

                    logger.info(f"✅ Connection obtained from pool (attempt {attempt + 1}/{retries})")
                    return conn

            # Fallback to direct connection if pool unavailable
            conn = psycopg2.connect(
                Config.DATABASE_URL,
                cursor_factory=RealDictCursor,
                connect_timeout=10
            )
            logger.info(f"✅ Direct connection established (attempt {attempt + 1}/{retries})")
            return conn

        except Exception as e:
            logger.error(f"❌ Connection attempt {attempt + 1}/{retries} failed: {str(e)}")

            # If not last attempt, wait before retrying
            if attempt < retries - 1:
                wait_time = delay * (attempt + 1)  # Exponential backoff
                logger.info(f"⏳ Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                # Last attempt failed
                error_msg = f"Failed to connect to database after {retries} attempts: {str(e)}"
                logger.error(f"❌ {error_msg}")
                raise Exception(error_msg)


def return_db_connection(conn):
    """
    Return connection to pool or close it safely
    Ensures proper cleanup to prevent pool exhaustion

    Args:
        conn: Database connection to return/close
    """
    global connection_pool

    if not conn:
        return

    try:
        # Rollback any uncommitted transactions
        try:
            conn.rollback()
        except Exception as rollback_error:
            logger.debug(f"Rollback on return (expected if already committed): {rollback_error}")

        # Return to pool or close
        if connection_pool:
            try:
                connection_pool.putconn(conn)
                logger.info("✅ Connection returned to pool")
            except Exception as putconn_error:
                logger.error(f"❌ Error returning to pool, forcing close: {putconn_error}")
                try:
                    conn.close()
                except:
                    pass
        else:
            conn.close()
            logger.info("✅ Direct connection closed")

    except Exception as e:
        logger.error(f"❌ Error in return_db_connection: {e}")
        # Force close as last resort
        try:
            conn.close()
        except:
            pass


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
    conn = None
    try:
        conn = get_db_connection(retries=3, delay=2)
        cursor = conn.cursor()

        cursor.execute("SELECT version();")
        version = cursor.fetchone()['version']

        cursor.execute("SELECT current_database();")
        db_name = cursor.fetchone()['current_database']

        cursor.close()

        return {
            'connected': True,
            'database': db_name,
            'version': version.split(',')[0],
            'pool_status': 'active' if connection_pool else 'inactive'
        }
    except Exception as e:
        return {
            'connected': False,
            'error': str(e),
            'pool_status': 'active' if connection_pool else 'inactive'
        }
    finally:
        if conn:
            return_db_connection(conn)
