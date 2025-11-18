"""
Authentication Routes for FNCS API
Handles user registration, login, token verification, and logout
"""

from flask import Blueprint, request, jsonify
import jwt
from datetime import datetime, timedelta
import psycopg2
from config import Config
from utils.db import get_db_connection, return_db_connection
from utils.password import hash_password, verify_password
from utils.validators import validate_email, validate_password

# Create authentication blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user

    Request Body:
        {
            "email": "user@example.com",
            "password": "securepassword",
            "full_name": "John Doe"
        }

    Returns:
        201: User created successfully
        400: Validation error or email already exists
        500: Server error
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400

        # Validate required fields
        required_fields = ['email', 'password', 'full_name']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'error': f'Field "{field}" is required'
                }), 400

        # Validate email
        email = data['email'].lower().strip()
        is_valid, error_msg = validate_email(email)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': error_msg
            }), 400

        # Validate password
        password = data['password']
        is_valid, error_msg = validate_password(password)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': error_msg
            }), 400

        # Validate full name
        full_name = data['full_name'].strip()
        if len(full_name) < 2:
            return jsonify({
                'success': False,
                'error': 'Full name must be at least 2 characters long'
            }), 400
        if len(full_name) > 100:
            return jsonify({
                'success': False,
                'error': 'Full name must not exceed 100 characters'
            }), 400

        # Hash password
        password_hash = hash_password(password)

        # Insert user into database
        conn = None
        try:
            conn = get_db_connection(retries=3, delay=2)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO users (email, password_hash, full_name)
                VALUES (%s, %s, %s)
                RETURNING id, email, full_name, created_at
            """, (email, password_hash, full_name))

            user = cursor.fetchone()
            conn.commit()
            cursor.close()

            return jsonify({
                'success': True,
                'message': 'User registered successfully',
                'data': {
                    'id': user['id'],
                    'email': user['email'],
                    'full_name': user['full_name'],
                    'created_at': user['created_at'].isoformat()
                }
            }), 201

        except psycopg2.IntegrityError as e:
            if 'unique constraint' in str(e).lower() or 'duplicate key' in str(e).lower():
                return jsonify({
                    'success': False,
                    'error': 'Email already registered'
                }), 400
            return jsonify({
                'success': False,
                'error': f'Database integrity error: {str(e)}'
            }), 400

        finally:
            if conn:
                return_db_connection(conn)

    except Exception as e:
        # Check if it's a connection error
        if 'Failed to connect' in str(e) or 'Network' in str(e):
            return jsonify({
                'success': False,
                'error': 'Database temporarily unavailable. Please try again in a moment.'
            }), 503
        return jsonify({
            'success': False,
            'error': f'Registration failed: {str(e)}'
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user and return JWT token

    Request Body:
        {
            "email": "user@example.com",
            "password": "securepassword"
        }

    Returns:
        200: Login successful with JWT token
        401: Invalid credentials or account deactivated
        400: Validation error
        500: Server error
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400

        # Validate required fields
        if 'email' not in data or 'password' not in data:
            return jsonify({
                'success': False,
                'error': 'Email and password are required'
            }), 400

        email = data['email'].lower().strip()
        password = data['password']

        if not email or not password:
            return jsonify({
                'success': False,
                'error': 'Email and password cannot be empty'
            }), 400

        # Get user from database
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, email, password_hash, full_name, is_active
            FROM users
            WHERE email = %s
        """, (email,))

        user = cursor.fetchone()
        cursor.close()
        conn.close()

        # Check if user exists
        if not user:
            return jsonify({
                'success': False,
                'error': 'Invalid email or password'
            }), 401

        # Check if account is active
        if not user['is_active']:
            return jsonify({
                'success': False,
                'error': 'Account is deactivated. Please contact support.'
            }), 401

        # Verify password
        if not verify_password(password, user['password_hash']):
            return jsonify({
                'success': False,
                'error': 'Invalid email or password'
            }), 401

        # Generate JWT token
        payload = {
            'user_id': user['id'],
            'email': user['email'],
            'exp': datetime.utcnow() + timedelta(seconds=Config.JWT_ACCESS_TOKEN_EXPIRES),
            'iat': datetime.utcnow()
        }

        token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)

        return jsonify({
            'success': True,
            'message': 'Login successful',
            'data': {
                'token': token,
                'user': {
                    'id': user['id'],
                    'email': user['email'],
                    'full_name': user['full_name']
                },
                'expires_in': Config.JWT_ACCESS_TOKEN_EXPIRES
            }
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Login failed: {str(e)}'
        }), 500


@auth_bp.route('/verify', methods=['GET'])
def verify_token():
    """
    Verify JWT token validity

    Headers:
        Authorization: Bearer <token>

    Returns:
        200: Token is valid
        401: Token is invalid, expired, or missing
    """
    token = None

    # Extract token from Authorization header
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        try:
            token = auth_header.split(" ")[1]
        except IndexError:
            return jsonify({
                'success': False,
                'error': 'Invalid authorization header format'
            }), 401

    if not token:
        return jsonify({
            'success': False,
            'error': 'Token is missing'
        }), 401

    try:
        # Decode and verify token
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])

        return jsonify({
            'success': True,
            'message': 'Token is valid',
            'data': {
                'user_id': payload['user_id'],
                'email': payload['email'],
                'expires_at': payload['exp']
            }
        }), 200

    except jwt.ExpiredSignatureError:
        return jsonify({
            'success': False,
            'error': 'Token has expired'
        }), 401
    except jwt.InvalidTokenError:
        return jsonify({
            'success': False,
            'error': 'Invalid token'
        }), 401
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Token verification failed: {str(e)}'
        }), 401


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    Logout endpoint

    Note: JWT tokens are stateless, so logout is handled client-side
    by removing the token from storage. This endpoint is provided for
    consistency and future server-side token blacklisting if needed.

    Returns:
        200: Logout successful
    """
    return jsonify({
        'success': True,
        'message': 'Logout successful. Please remove token from client storage.'
    }), 200


@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """
    Get current user information (requires authentication)

    Headers:
        Authorization: Bearer <token>

    Returns:
        200: User information
        401: Invalid or missing token
    """
    from middleware.auth_middleware import token_required

    @token_required
    def _get_user():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, email, full_name, is_active, created_at
                FROM users
                WHERE id = %s
            """, (request.user_id,))

            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if not user:
                return jsonify({
                    'success': False,
                    'error': 'User not found'
                }), 404

            return jsonify({
                'success': True,
                'data': {
                    'id': user['id'],
                    'email': user['email'],
                    'full_name': user['full_name'],
                    'is_active': user['is_active'],
                    'created_at': user['created_at'].isoformat()
                }
            }), 200

        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Failed to retrieve user: {str(e)}'
            }), 500

    return _get_user()
