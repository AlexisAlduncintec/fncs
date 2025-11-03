"""
Configuration Management for FNCS API
Centralized configuration for environment variables and app settings
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration class"""

    # Database Configuration
    DATABASE_URL = os.getenv('DATABASE_URL')

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))  # 1 hour

    # Flask Configuration
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    ENV = os.getenv('FLASK_ENV', 'development')

    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')

    @staticmethod
    def validate():
        """Validate required configuration variables"""
        required = ['DATABASE_URL', 'JWT_SECRET_KEY']
        missing = [key for key in required if not getattr(Config, key)]

        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

        # Warning for default JWT secret in production
        if Config.ENV == 'production' and Config.JWT_SECRET_KEY == 'dev-secret-key-change-in-production':
            raise ValueError("JWT_SECRET_KEY must be changed in production environment!")

        return True

    @staticmethod
    def get_info():
        """Get configuration information for logging"""
        return {
            'environment': Config.ENV,
            'debug': Config.DEBUG,
            'jwt_expires': f"{Config.JWT_ACCESS_TOKEN_EXPIRES}s",
            'cors_origins': Config.CORS_ORIGINS,
            'database': 'Connected' if Config.DATABASE_URL else 'Not configured'
        }
