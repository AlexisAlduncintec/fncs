"""
Category Routes for FNCS API
Handles CRUD operations for categories (Protected with JWT)
"""

from flask import Blueprint, request, jsonify
import psycopg2
from middleware.auth_middleware import token_required
from utils.db import get_db_connection
from utils.validators import validate_category_data

# Create categories blueprint
category_bp = Blueprint('categories', __name__, url_prefix='/categories')


@category_bp.route('', methods=['GET'])
@token_required
def get_categories():
    """
    Get all categories (Protected)

    Headers:
        Authorization: Bearer <token>

    Returns:
        200: List of all categories
        401: Unauthorized (invalid/missing token)
        500: Server error
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


@category_bp.route('/<int:category_id>', methods=['GET'])
@token_required
def get_category(category_id):
    """
    Get a specific category by ID (Protected)

    Args:
        category_id (int): Category ID

    Headers:
        Authorization: Bearer <token>

    Returns:
        200: Category data
        401: Unauthorized (invalid/missing token)
        404: Category not found
        500: Server error
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


@category_bp.route('', methods=['POST'])
@token_required
def create_category():
    """
    Create a new category (Protected)

    Headers:
        Authorization: Bearer <token>

    Request Body:
        {
            "name": "Category Name",
            "description": "Optional description",
            "is_active": true
        }

    Returns:
        201: Category created successfully
        400: Validation error or duplicate name
        401: Unauthorized (invalid/missing token)
        500: Server error
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


@category_bp.route('/<int:category_id>', methods=['PUT'])
@token_required
def update_category(category_id):
    """
    Update a category (Protected)

    Args:
        category_id (int): Category ID

    Headers:
        Authorization: Bearer <token>

    Request Body:
        {
            "name": "Updated Name",
            "description": "Updated description",
            "is_active": false
        }

    Returns:
        200: Category updated successfully
        400: Validation error or duplicate name
        401: Unauthorized (invalid/missing token)
        404: Category not found
        500: Server error
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

        if len(update_fields) == 1:  # Only updated_at
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


@category_bp.route('/<int:category_id>', methods=['DELETE'])
@token_required
def delete_category(category_id):
    """
    Delete a category (Protected)

    Args:
        category_id (int): Category ID

    Headers:
        Authorization: Bearer <token>

    Returns:
        200: Category deleted successfully
        401: Unauthorized (invalid/missing token)
        404: Category not found
        500: Server error
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
