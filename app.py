"""
Financial News Classification System (FNCS) - REST API v2.0
Flask application with JWT authentication and CRUD operations
"""

from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from routes.auth_routes import auth_bp
from routes.category_routes import category_bp
import re

# Validate configuration before starting
try:
    Config.validate()
except ValueError as e:
    print(f"Configuration Error: {e}")
    print("Please check your .env file and ensure all required variables are set.")
    exit(1)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Configure CORS with support for Render and Vercel domains
def cors_origin_validator(origin):
    """
    Custom CORS origin validator supporting wildcards for Render and Vercel
    """
    # Allow localhost origins
    if origin in Config.CORS_ORIGINS:
        return True

    # Allow Render domains
    if re.match(r'https://[\w-]+\.onrender\.com', origin):
        return True

    # Allow Vercel domains
    if re.match(r'https://[\w-]+\.vercel\.app', origin):
        return True

    return False

CORS(app, resources={
    r"/*": {
        "origins": cors_origin_validator,
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True,
        "max_age": 3600
    }
})

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(category_bp)


# Root endpoint
@app.route('/', methods=['GET'])
def root():
    """
    API root endpoint - provides information about available endpoints
    """
    return jsonify({
        'success': True,
        'message': 'FNCS API - Financial News Classification System',
        'version': '2.0.0',
        'documentation': {
            'authentication': 'JWT Bearer token required for protected endpoints',
            'base_url': 'http://localhost:5000'
        },
        'endpoints': {
            'auth': {
                'register': {
                    'method': 'POST',
                    'path': '/auth/register',
                    'description': 'Register a new user',
                    'protected': False
                },
                'login': {
                    'method': 'POST',
                    'path': '/auth/login',
                    'description': 'Login and get JWT token',
                    'protected': False
                },
                'verify': {
                    'method': 'GET',
                    'path': '/auth/verify',
                    'description': 'Verify JWT token validity',
                    'protected': False
                },
                'me': {
                    'method': 'GET',
                    'path': '/auth/me',
                    'description': 'Get current user information',
                    'protected': True
                },
                'logout': {
                    'method': 'POST',
                    'path': '/auth/logout',
                    'description': 'Logout (client-side token removal)',
                    'protected': False
                }
            },
            'categories': {
                'list': {
                    'method': 'GET',
                    'path': '/categories',
                    'description': 'Get all categories',
                    'protected': True
                },
                'get': {
                    'method': 'GET',
                    'path': '/categories/<id>',
                    'description': 'Get category by ID',
                    'protected': True
                },
                'create': {
                    'method': 'POST',
                    'path': '/categories',
                    'description': 'Create new category',
                    'protected': True
                },
                'update': {
                    'method': 'PUT',
                    'path': '/categories/<id>',
                    'description': 'Update category',
                    'protected': True
                },
                'delete': {
                    'method': 'DELETE',
                    'path': '/categories/<id>',
                    'description': 'Delete category',
                    'protected': True
                }
            }
        }
    }), 200


# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint for monitoring
    """
    from utils.db import test_connection

    db_status = test_connection()

    return jsonify({
        'success': True,
        'status': 'healthy',
        'database': db_status,
        'config': Config.get_info()
    }), 200


# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'message': 'The requested URL was not found on the server. Check the API documentation at /'
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        'success': False,
        'error': 'Method not allowed',
        'message': 'The method is not allowed for the requested URL'
    }), 405


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'message': 'An internal server error occurred. Please try again later.'
    }), 500


if __name__ == '__main__':
    import os
    config_info = Config.get_info()

    # Get port from environment variable (Render) or use default for local dev
    port = int(os.getenv('PORT', 5001))

    print("=" * 80)
    print("FNCS API v2.0 - Financial News Classification System")
    print("=" * 80)
    print(f"Environment: {config_info['environment']}")
    print(f"Debug Mode: {config_info['debug']}")
    print(f"Server: http://0.0.0.0:{port}")
    print(f"Database: {config_info['database']}")
    print(f"JWT Token Expires: {config_info['jwt_expires']}")
    print(f"CORS Origins: {', '.join(config_info['cors_origins'])}")
    print("=" * 80)
    print("\nAuthentication Endpoints:")
    print("  POST   /auth/register       - Register new user")
    print("  POST   /auth/login          - Login and get JWT token")
    print("  GET    /auth/verify         - Verify token validity")
    print("  GET    /auth/me             - Get current user info (protected)")
    print("  POST   /auth/logout         - Logout")
    print("\nCategory Endpoints (Protected - JWT Required):")
    print("  GET    /categories          - Get all categories")
    print("  GET    /categories/<id>     - Get category by ID")
    print("  POST   /categories          - Create new category")
    print("  PUT    /categories/<id>     - Update category")
    print("  DELETE /categories/<id>     - Delete category")
    print("\nUtility Endpoints:")
    print("  GET    /                    - API documentation")
    print("  GET    /health              - Health check")
    print("=" * 80)
    print("\nStarting server...")
    print("=" * 80)

    app.run(debug=Config.DEBUG, host='0.0.0.0', port=port)
