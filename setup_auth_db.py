"""
Authentication Database Setup Script for FNCS
==============================================
This script sets up the users table in Supabase PostgreSQL by:
1. Testing the database connection
2. Creating the users table
3. Verifying the setup
"""

import os
import sys
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(f"{Colors.HEADER}{Colors.BOLD}{text}{Colors.ENDC}")
    print("=" * 80)


def print_success(text):
    """Print success message"""
    print(f"{Colors.OKGREEN}[OK] {text}{Colors.ENDC}")


def print_error(text):
    """Print error message"""
    print(f"{Colors.FAIL}[ERROR] {text}{Colors.ENDC}")


def print_info(text):
    """Print info message"""
    print(f"{Colors.OKCYAN}[INFO] {text}{Colors.ENDC}")


def print_warning(text):
    """Print warning message"""
    print(f"{Colors.WARNING}[WARNING] {text}{Colors.ENDC}")


def load_environment():
    """Load environment variables from .env file"""
    print_header("STEP 1: Loading Environment Variables")

    if not os.path.exists('.env'):
        print_error(".env file not found!")
        print_info("Please create a .env file with your DATABASE_URL")
        return None

    load_dotenv()
    database_url = os.getenv('DATABASE_URL')

    if not database_url:
        print_error("DATABASE_URL not found in .env file")
        return None

    # Mask password in output
    masked_url = database_url
    if '@' in database_url and ':' in database_url:
        parts = database_url.split('@')
        credentials = parts[0].split(':')
        if len(credentials) > 2:
            masked_password = credentials[2][:3] + "*" * (len(credentials[2]) - 3)
            masked_url = f"{credentials[0]}:{credentials[1]}:{masked_password}@{parts[1]}"

    print_success("Environment variables loaded successfully")
    print_info(f"Database URL: {masked_url}")

    return database_url


def test_connection(database_url):
    """Test database connection"""
    print_header("STEP 2: Testing Database Connection")

    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()

        # Get PostgreSQL version
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]

        # Get current database name
        cursor.execute("SELECT current_database();")
        db_name = cursor.fetchone()[0]

        # Get current user
        cursor.execute("SELECT current_user;")
        db_user = cursor.fetchone()[0]

        print_success("Database connection successful!")
        print_info(f"Database: {db_name}")
        print_info(f"User: {db_user}")
        print_info(f"PostgreSQL Version: {version.split(',')[0]}")

        cursor.close()
        conn.close()
        return True

    except psycopg2.OperationalError as e:
        print_error("Connection failed!")
        print_error(f"Error: {str(e)}")
        print_warning("Please check:")
        print("  - Your internet connection")
        print("  - DATABASE_URL is correct in .env file")
        print("  - Supabase project is active")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        return False


def execute_sql_file(database_url, sql_file_path):
    """Execute SQL script from file"""
    print_header("STEP 3: Creating Users Table")

    if not os.path.exists(sql_file_path):
        print_error(f"SQL file not found: {sql_file_path}")
        return False

    try:
        # Read SQL file
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        print_info(f"Reading SQL script: {sql_file_path}")

        # Connect and execute
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()

        print_info("Executing SQL script...")
        cursor.execute(sql_script)
        conn.commit()

        print_success("SQL script executed successfully!")
        print_success("Users table created")
        print_success("Indexes created")
        print_success("Triggers created")

        cursor.close()
        conn.close()
        return True

    except psycopg2.Error as e:
        print_error("SQL execution failed!")
        print_error(f"Error: {str(e)}")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        return False


def verify_setup(database_url):
    """Verify table creation"""
    print_header("STEP 4: Verifying Database Setup")

    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()

        # Check if table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_name = 'users'
            );
        """)
        table_exists = cursor.fetchone()[0]

        if not table_exists:
            print_error("Users table does not exist!")
            cursor.close()
            conn.close()
            return False

        print_success("Users table exists")

        # Get table structure
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = 'users'
            ORDER BY ordinal_position;
        """)
        columns = cursor.fetchall()

        print_info("Table structure:")
        for col in columns:
            nullable = "NULL" if col[1] == "YES" else "NOT NULL"
            default = f"DEFAULT {col[3]}" if col[3] else ""
            print(f"  - {col[0]}: {col[1]} {nullable} {default}")

        # Count records
        cursor.execute("SELECT COUNT(*) FROM users;")
        count = cursor.fetchone()[0]
        print_success(f"Total users: {count}")

        # Check indexes
        cursor.execute("""
            SELECT indexname
            FROM pg_indexes
            WHERE tablename = 'users';
        """)
        indexes = cursor.fetchall()

        print_success(f"Indexes created: {len(indexes)}")
        for idx in indexes:
            print(f"  - {idx[0]}")

        # Check triggers
        cursor.execute("""
            SELECT trigger_name
            FROM information_schema.triggers
            WHERE event_object_table = 'users';
        """)
        triggers = cursor.fetchall()

        if triggers:
            print_success(f"Triggers created: {len(triggers)}")
            for trg in triggers:
                print(f"  - {trg[0]}")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print_error(f"Verification failed: {str(e)}")
        return False


def main():
    """Main setup function"""
    print_header("FNCS Authentication Database Setup - Starting")
    print_info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Step 1: Load environment
    database_url = load_environment()
    if not database_url:
        print_error("Setup failed: Could not load environment variables")
        return False

    # Step 2: Test connection
    if not test_connection(database_url):
        print_error("Setup failed: Could not connect to database")
        print_warning("\nTroubleshooting steps:")
        print("1. Check your internet connection")
        print("2. Verify DATABASE_URL in .env file")
        print("3. Ensure Supabase project is active")
        print("4. Check firewall settings")
        return False

    # Step 3: Execute SQL script
    if not execute_sql_file(database_url, 'create_users_table.sql'):
        print_error("Setup failed: Could not create users table")
        return False

    # Step 4: Verify setup
    if not verify_setup(database_url):
        print_error("Setup failed: Verification failed")
        return False

    # Success summary
    print_header("SETUP COMPLETED SUCCESSFULLY!")
    print_success("Users table is ready for authentication")
    print_info("\nNext steps:")
    print("1. Install new dependencies: pip install -r requirements.txt")
    print("2. Start the Flask API: python app.py")
    print("3. Test authentication endpoints:")
    print("   - POST /auth/register - Register a new user")
    print("   - POST /auth/login - Login and get JWT token")
    print("   - GET /auth/verify - Verify token")
    print("\nAPI will be available at: http://localhost:5000")
    print("=" * 80 + "\n")

    return True


if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print_warning("\n\nSetup interrupted by user")
        exit(1)
    except Exception as e:
        print_error(f"\nUnexpected error: {str(e)}")
        exit(1)
