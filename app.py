"""
Financial News Classification System (FNCS) - Categories REST API
Flask application providing CRUD operations for categories table
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")


def get_db_connection():
    """
    Establish and return a database connection

    Returns:
        psycopg2.connection: Database connection object

    Raises:
        Exception: If connection fails
    """
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        raise Exception(f"Database connection failed: {str(e)}")


def validate_category_data(data, is_update=False):
    """
    Validate category data for POST and PUT requests

    Args:
        data (dict): Category data to validate
        is_update (bool): Whether this is an update operation

    Returns:
        tuple: (is_valid, error_message)
    """
    if not is_update and 'name' not in data:
        return False, "Field 'name' is required"

    if 'name' in data:
        if not data['name'] or not isinstance(data['name'], str):
            return False, "Field 'name' must be a non-empty string"
        if len(data['name']) > 100:
            return False, "Field 'name' must not exceed 100 characters"

    if 'description' in data and data['description'] is not None:
        if not isinstance(data['description'], str):
            return False, "Field 'description' must be a string"

    if 'is_active' in data and data['is_active'] is not None:
        if not isinstance(data['is_active'], bool):
            return False, "Field 'is_active' must be a boolean"

    return True, None


@app.route('/categories', methods=['GET'])
def get_categories():
    """
    Get all categories

    Returns:
        JSON: List of all categories with 200 status code
        JSON: Error message with appropriate status code on failure
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, description, is_active, created_at, updated_at
            FROM categories
            ORDER BY id ASC
        """)

        categories = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({
            'success': True,
            'data': categories,
            'count': len(categories)
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to retrieve categories: {str(e)}'
        }), 500


@app.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """
    Get a specific category by ID

    Args:
        category_id (int): Category ID

    Returns:
        JSON: Category data with 200 status code
        JSON: Error message with 404 if not found or 500 on failure
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, description, is_active, created_at, updated_at
            FROM categories
            WHERE id = %s
        """, (category_id,))

        category = cursor.fetchone()

        cursor.close()
        conn.close()

        if category is None:
            return jsonify({
                'success': False,
                'error': f'Category with id {category_id} not found'
            }), 404

        return jsonify({
            'success': True,
            'data': category
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to retrieve category: {str(e)}'
        }), 500


@app.route('/categories', methods=['POST'])
def create_category():
    """
    Create a new category

    Expected JSON body:
        - name (required): Category name (max 100 chars)
        - description (optional): Category description
        - is_active (optional): Boolean, defaults to true

    Returns:
        JSON: Created category data with 201 status code
        JSON: Error message with 400 for validation errors or 500 on failure
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400

        # Validate data
        is_valid, error_message = validate_category_data(data)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': error_message
            }), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert new category
        cursor.execute("""
            INSERT INTO categories (name, description, is_active)
            VALUES (%s, %s, %s)
            RETURNING id, name, description, is_active, created_at, updated_at
        """, (
            data['name'],
            data.get('description'),
            data.get('is_active', True)
        ))

        new_category = cursor.fetchone()

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            'success': True,
            'message': 'Category created successfully',
            'data': new_category
        }), 201

    except psycopg2.IntegrityError as e:
        if 'unique constraint' in str(e).lower():
            return jsonify({
                'success': False,
                'error': 'A category with this name already exists'
            }), 400
        return jsonify({
            'success': False,
            'error': f'Database integrity error: {str(e)}'
        }), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to create category: {str(e)}'
        }), 500


@app.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    """
    Update a complete category

    Args:
        category_id (int): Category ID

    Expected JSON body:
        - name (optional): Category name (max 100 chars)
        - description (optional): Category description
        - is_active (optional): Boolean

    Returns:
        JSON: Updated category data with 200 status code
        JSON: Error message with 404 if not found, 400 for validation errors, or 500 on failure
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400

        # Validate data
        is_valid, error_message = validate_category_data(data, is_update=True)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': error_message
            }), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if category exists
        cursor.execute("SELECT id FROM categories WHERE id = %s", (category_id,))
        if cursor.fetchone() is None:
            cursor.close()
            conn.close()
            return jsonify({
                'success': False,
                'error': f'Category with id {category_id} not found'
            }), 404

        # Build dynamic UPDATE query based on provided fields
        update_fields = []
        update_values = []

        if 'name' in data:
            update_fields.append("name = %s")
            update_values.append(data['name'])

        if 'description' in data:
            update_fields.append("description = %s")
            update_values.append(data['description'])

        if 'is_active' in data:
            update_fields.append("is_active = %s")
            update_values.append(data['is_active'])

        # Always update the updated_at field
        update_fields.append("updated_at = NOW()")

        if not update_fields:
            cursor.close()
            conn.close()
            return jsonify({
                'success': False,
                'error': 'No valid fields to update'
            }), 400

        # Add category_id to values for WHERE clause
        update_values.append(category_id)

        # Execute UPDATE query
        update_query = f"""
            UPDATE categories
            SET {', '.join(update_fields)}
            WHERE id = %s
            RETURNING id, name, description, is_active, created_at, updated_at
        """

        cursor.execute(update_query, update_values)
        updated_category = cursor.fetchone()

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            'success': True,
            'message': 'Category updated successfully',
            'data': updated_category
        }), 200

    except psycopg2.IntegrityError as e:
        if 'unique constraint' in str(e).lower():
            return jsonify({
                'success': False,
                'error': 'A category with this name already exists'
            }), 400
        return jsonify({
            'success': False,
            'error': f'Database integrity error: {str(e)}'
        }), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to update category: {str(e)}'
        }), 500


@app.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    """
    Delete a category

    Args:
        category_id (int): Category ID

    Returns:
        JSON: Success message with 200 status code
        JSON: Error message with 404 if not found or 500 on failure
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if category exists
        cursor.execute("SELECT id, name FROM categories WHERE id = %s", (category_id,))
        category = cursor.fetchone()

        if category is None:
            cursor.close()
            conn.close()
            return jsonify({
                'success': False,
                'error': f'Category with id {category_id} not found'
            }), 404

        # Delete the category
        cursor.execute("DELETE FROM categories WHERE id = %s", (category_id,))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            'success': True,
            'message': f'Category "{category["name"]}" deleted successfully'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to delete category: {str(e)}'
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        'success': False,
        'error': 'Method not allowed'
    }), 405


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("FNCS Categories API - Starting server")
    print("=" * 60)
    print(f"Server running on: http://localhost:5000")
    print(f"Database connected: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'configured'}")
    print("\nAvailable endpoints:")
    print("  GET    /categories          - Get all categories")
    print("  GET    /categories/<id>     - Get category by ID")
    print("  POST   /categories          - Create new category")
    print("  PUT    /categories/<id>     - Update category")
    print("  DELETE /categories/<id>     - Delete category")
    print("=" * 60)

    app.run(debug=True, host='0.0.0.0', port=5000)
