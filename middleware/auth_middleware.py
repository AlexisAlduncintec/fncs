"""
JWT Authentication Middleware
Provides decorator for protecting routes with JWT authentication
"""

import jwt
from functools import wraps
from flask import request, jsonify
from config import Config


def token_required(f):
    """
    Decorator to protect routes with JWT authentication

    Usage:
        @app.route('/protected')
        @token_required
        def protected_route():
            user_id = request.user_id
            return jsonify({'message': f'Hello user {user_id}'})

    The decorator adds the following attributes to the request object:
        - request.user_id: The authenticated user's ID
        - request.user_email: The authenticated user's email

    Returns:
        401: If token is missing, invalid, or expired
        Original function response: If token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Extract token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                # Expected format: "Bearer <token>"
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid authorization header format. Use: Bearer <token>'
                }), 401

        # Check if token exists
        if not token:
            return jsonify({
                'success': False,
                'error': 'Authentication token is missing'
            }), 401

        try:
            # Decode and verify token
            payload = jwt.decode(
                token,
                Config.JWT_SECRET_KEY,
                algorithms=[Config.JWT_ALGORITHM]
            )

            # Add user info to request object
            request.user_id = payload['user_id']
            request.user_email = payload['email']

        except jwt.ExpiredSignatureError:
            return jsonify({
                'success': False,
                'error': 'Token has expired. Please login again.'
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                'success': False,
                'error': 'Invalid token. Authentication failed.'
            }), 401
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Token verification failed: {str(e)}'
            }), 401

        # Call the original function if token is valid
        return f(*args, **kwargs)

    return decorated


def optional_token(f):
    """
    Decorator for routes where authentication is optional

    Adds user info to request if token is present and valid,
    but doesn't reject the request if token is missing

    Usage:
        @app.route('/public-with-user-info')
        @optional_token
        def public_route():
            if hasattr(request, 'user_id'):
                return jsonify({'message': 'Logged in user'})
            else:
                return jsonify({'message': 'Anonymous user'})
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                pass  # Ignore invalid format for optional auth

        if token:
            try:
                payload = jwt.decode(
                    token,
                    Config.JWT_SECRET_KEY,
                    algorithms=[Config.JWT_ALGORITHM]
                )
                request.user_id = payload['user_id']
                request.user_email = payload['email']
            except Exception:
                pass  # Ignore token errors for optional auth

        return f(*args, **kwargs)

    return decorated
