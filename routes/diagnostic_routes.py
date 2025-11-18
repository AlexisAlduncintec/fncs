"""
Diagnostic Routes for Database Connection Testing
Helps identify exactly where database connection failures occur
"""

from flask import Blueprint, jsonify
import psycopg2
import os
import socket

diagnostic_bp = Blueprint('diagnostic', __name__)

@diagnostic_bp.route('/diagnostic/db-test', methods=['GET'])
def test_database():
    """Comprehensive database connection test"""
    DATABASE_URL = os.environ.get('DATABASE_URL')

    result = {
        'database_url_exists': bool(DATABASE_URL),
        'connection_string_format': 'valid' if DATABASE_URL and DATABASE_URL.startswith('postgresql://') else 'invalid',
        'tests': []
    }

    if not DATABASE_URL:
        return jsonify({'success': False, 'error': 'DATABASE_URL not set', 'result': result}), 500

    # Extract host and port
    try:
        parts = DATABASE_URL.split('@')[1].split('/')[0]
        host = parts.split(':')[0]
        port = int(parts.split(':')[1]) if ':' in parts else 5432

        # Test 1: DNS Resolution
        try:
            ip = socket.gethostbyname(host)
            result['tests'].append({
                'name': 'DNS Resolution',
                'status': 'PASS',
                'details': f'Resolved {host} to {ip}'
            })
        except Exception as e:
            result['tests'].append({
                'name': 'DNS Resolution',
                'status': 'FAIL',
                'details': str(e)
            })
            return jsonify({'success': False, 'result': result}), 500

        # Test 2: TCP Connection
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((host, port))
            sock.close()
            result['tests'].append({
                'name': 'TCP Connection',
                'status': 'PASS',
                'details': f'Connected to {host}:{port}'
            })
        except Exception as e:
            result['tests'].append({
                'name': 'TCP Connection',
                'status': 'FAIL',
                'details': str(e)
            })
            return jsonify({'success': False, 'result': result}), 500

        # Test 3: PostgreSQL Connection
        try:
            conn = psycopg2.connect(DATABASE_URL, connect_timeout=10)
            conn.close()
            result['tests'].append({
                'name': 'PostgreSQL Connection',
                'status': 'PASS',
                'details': 'Successfully connected to database'
            })
        except Exception as e:
            result['tests'].append({
                'name': 'PostgreSQL Connection',
                'status': 'FAIL',
                'details': str(e)
            })
            return jsonify({'success': False, 'result': result}), 500

        # Test 4: Query Execution
        try:
            conn = psycopg2.connect(DATABASE_URL, connect_timeout=10)
            cur = conn.cursor()
            cur.execute('SELECT 1')
            cur.close()
            conn.close()
            result['tests'].append({
                'name': 'Query Execution',
                'status': 'PASS',
                'details': 'Successfully executed test query'
            })
        except Exception as e:
            result['tests'].append({
                'name': 'Query Execution',
                'status': 'FAIL',
                'details': str(e)
            })
            return jsonify({'success': False, 'result': result}), 500

        return jsonify({'success': True, 'result': result}), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'result': result}), 500

@diagnostic_bp.route('/diagnostic/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'message': 'API is running'
    }), 200
