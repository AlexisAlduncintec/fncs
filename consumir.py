"""
API Consumer Script for FNCS Categories API
Provides functions to interact with all CRUD endpoints
"""

import requests
import json
from typing import Dict, Optional

# API Base URL
BASE_URL = "http://localhost:5000"


def print_response(response: requests.Response, operation: str):
    """
    Pretty print API response

    Args:
        response: HTTP response object
        operation: Description of the operation
    """
    print("\n" + "=" * 80)
    print(f"OPERATION: {operation}")
    print("=" * 80)
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print("-" * 80)

    try:
        json_response = response.json()
        print(json.dumps(json_response, indent=2, ensure_ascii=False))
    except json.JSONDecodeError:
        print(response.text)

    print("=" * 80)


def get_all_categories():
    """
    Get all categories from the API

    Returns:
        dict: JSON response with all categories
    """
    try:
        print("\nFetching all categories...")
        response = requests.get(f"{BASE_URL}/categories")
        print_response(response, "GET ALL CATEGORIES")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")
        return None


def get_category_by_id(category_id: int):
    """
    Get a specific category by ID

    Args:
        category_id: The ID of the category to retrieve

    Returns:
        dict: JSON response with category data
    """
    try:
        print(f"\nFetching category with ID {category_id}...")
        response = requests.get(f"{BASE_URL}/categories/{category_id}")
        print_response(response, f"GET CATEGORY BY ID ({category_id})")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")
        return None


def create_category(data: Dict):
    """
    Create a new category

    Args:
        data: Dictionary with category data
              Required: name
              Optional: description, is_active

    Returns:
        dict: JSON response with created category
    """
    try:
        print(f"\nCreating new category...")
        print(f"Data: {json.dumps(data, indent=2, ensure_ascii=False)}")

        response = requests.post(
            f"{BASE_URL}/categories",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        print_response(response, "CREATE CATEGORY")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")
        return None


def update_category(category_id: int, data: Dict):
    """
    Update an existing category

    Args:
        category_id: The ID of the category to update
        data: Dictionary with updated category data
              Optional: name, description, is_active

    Returns:
        dict: JSON response with updated category
    """
    try:
        print(f"\nUpdating category with ID {category_id}...")
        print(f"Data: {json.dumps(data, indent=2, ensure_ascii=False)}")

        response = requests.put(
            f"{BASE_URL}/categories/{category_id}",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        print_response(response, f"UPDATE CATEGORY ({category_id})")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")
        return None


def delete_category(category_id: int):
    """
    Delete a category

    Args:
        category_id: The ID of the category to delete

    Returns:
        dict: JSON response with deletion confirmation
    """
    try:
        print(f"\nDeleting category with ID {category_id}...")
        response = requests.delete(f"{BASE_URL}/categories/{category_id}")
        print_response(response, f"DELETE CATEGORY ({category_id})")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")
        return None


def run_demo():
    """
    Run a complete demo of all API endpoints
    """
    print("\n" + "=" * 80)
    print("FNCS CATEGORIES API - CONSUMPTION DEMO")
    print("=" * 80)
    print("This script will demonstrate all CRUD operations")
    print("=" * 80)

    # 1. Get all categories (initial state)
    print("\n\n1. GETTING ALL CATEGORIES (Initial State)")
    get_all_categories()

    # 2. Create a new category
    print("\n\n2. CREATING A NEW CATEGORY")
    new_category_data = {
        "name": "Technology",
        "description": "News related to technology, software, and hardware",
        "is_active": True
    }
    created = create_category(new_category_data)

    # Extract the created category ID for subsequent operations
    category_id = None
    if created and created.get('success') and 'data' in created:
        category_id = created['data']['id']

    # 3. Get the newly created category by ID
    if category_id:
        print("\n\n3. GETTING CATEGORY BY ID")
        get_category_by_id(category_id)

    # 4. Create another category
    print("\n\n4. CREATING ANOTHER CATEGORY")
    second_category_data = {
        "name": "Finance",
        "description": "Financial markets, stocks, and economic news",
        "is_active": True
    }
    create_category(second_category_data)

    # 5. Get all categories (after creating two)
    print("\n\n5. GETTING ALL CATEGORIES (After Creating Two)")
    get_all_categories()

    # 6. Update the first category
    if category_id:
        print("\n\n6. UPDATING CATEGORY")
        update_data = {
            "name": "Tech & Innovation",
            "description": "Updated: Technology, innovation, and digital transformation news",
            "is_active": True
        }
        update_category(category_id, update_data)

    # 7. Get the updated category
    if category_id:
        print("\n\n7. GETTING UPDATED CATEGORY")
        get_category_by_id(category_id)

    # 8. Test partial update
    if category_id:
        print("\n\n8. TESTING PARTIAL UPDATE (only description)")
        partial_update = {
            "description": "Partial update: Only description changed"
        }
        update_category(category_id, partial_update)

    # 9. Deactivate category
    if category_id:
        print("\n\n9. DEACTIVATING CATEGORY")
        deactivate_data = {
            "is_active": False
        }
        update_category(category_id, deactivate_data)

    # 10. Delete the category
    if category_id:
        print("\n\n10. DELETING CATEGORY")
        delete_category(category_id)

    # 11. Try to get deleted category (should return 404)
    if category_id:
        print("\n\n11. TRYING TO GET DELETED CATEGORY (Should return 404)")
        get_category_by_id(category_id)

    # 12. Get all categories (final state)
    print("\n\n12. GETTING ALL CATEGORIES (Final State)")
    get_all_categories()

    # 13. Test error cases
    print("\n\n13. TESTING ERROR CASES")

    print("\n13.1. Creating category without required 'name' field:")
    create_category({"description": "Missing name field"})

    print("\n13.2. Creating duplicate category:")
    create_category({"name": "Finance", "description": "Duplicate name"})

    print("\n13.3. Getting non-existent category (ID 99999):")
    get_category_by_id(99999)

    print("\n13.4. Updating non-existent category:")
    update_category(99999, {"name": "Non-existent"})

    print("\n13.5. Deleting non-existent category:")
    delete_category(99999)

    print("\n\n" + "=" * 80)
    print("DEMO COMPLETED!")
    print("=" * 80)


def interactive_menu():
    """
    Interactive menu for manual API testing
    """
    while True:
        print("\n" + "=" * 80)
        print("FNCS CATEGORIES API - INTERACTIVE MENU")
        print("=" * 80)
        print("1. Get all categories")
        print("2. Get category by ID")
        print("3. Create new category")
        print("4. Update category")
        print("5. Delete category")
        print("6. Run full demo")
        print("0. Exit")
        print("=" * 80)

        choice = input("\nSelect an option: ").strip()

        if choice == "0":
            print("\nExiting... Goodbye!")
            break

        elif choice == "1":
            get_all_categories()

        elif choice == "2":
            try:
                category_id = int(input("Enter category ID: "))
                get_category_by_id(category_id)
            except ValueError:
                print("Error: Invalid ID format")

        elif choice == "3":
            name = input("Enter category name: ").strip()
            description = input("Enter description (optional): ").strip()
            is_active = input("Is active? (y/n, default=y): ").strip().lower() != 'n'

            data = {"name": name, "is_active": is_active}
            if description:
                data["description"] = description

            create_category(data)

        elif choice == "4":
            try:
                category_id = int(input("Enter category ID to update: "))
                print("\nLeave fields empty to skip updating them")
                name = input("Enter new name (optional): ").strip()
                description = input("Enter new description (optional): ").strip()
                is_active_input = input("Is active? (y/n/skip): ").strip().lower()

                data = {}
                if name:
                    data["name"] = name
                if description:
                    data["description"] = description
                if is_active_input in ['y', 'n']:
                    data["is_active"] = is_active_input == 'y'

                if data:
                    update_category(category_id, data)
                else:
                    print("No fields to update")

            except ValueError:
                print("Error: Invalid ID format")

        elif choice == "5":
            try:
                category_id = int(input("Enter category ID to delete: "))
                confirm = input(f"Are you sure you want to delete category {category_id}? (y/n): ").strip().lower()
                if confirm == 'y':
                    delete_category(category_id)
                else:
                    print("Deletion cancelled")
            except ValueError:
                print("Error: Invalid ID format")

        elif choice == "6":
            run_demo()

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("FNCS CATEGORIES API CONSUMER")
    print("=" * 80)
    print("Make sure the Flask API is running on http://localhost:5000")
    print("=" * 80)

    mode = input("\nSelect mode:\n1. Interactive Menu\n2. Run Full Demo\n\nChoice: ").strip()

    if mode == "1":
        interactive_menu()
    elif mode == "2":
        run_demo()
    else:
        print("Invalid choice. Running interactive menu by default...")
        interactive_menu()
