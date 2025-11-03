# FNCS - Financial News Classification System
## Categories CRUD API

REST API backend built with Python Flask for managing categories in the Financial News Classification System. Provides complete CRUD operations with PostgreSQL database on Supabase.

---

## 🚀 Quick Setup (Start Here!)

**Get your API running in 3 minutes:**

### 1. Install Dependencies
```bash
# Create and activate virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install required packages
pip install -r requirements.txt
```

### 2. Configure Database
The `.env` file is already configured with your Supabase credentials. No changes needed!

### 3. Set Up Database Table
```bash
python setup_db.py
```

This script will:
- ✅ Test your Supabase connection
- ✅ Create the `categories` table
- ✅ Add indexes and triggers
- ✅ Insert 10 sample categories
- ✅ Verify everything is working

**Expected Output:**
```
============================================================
FNCS Database Setup - Starting
============================================================
✅ Environment variables loaded successfully
✅ Database connection successful!
✅ Categories table created
✅ Total categories: 10
============================================================
SETUP COMPLETED SUCCESSFULLY! 🎉
============================================================
```

### 4. Start the API
```bash
python app.py
```

Access your API at: **http://localhost:5000/categories**

### 5. Test Everything
```bash
python consumir.py
```

Choose option **2** for a full demo or option **1** for interactive testing.

---

### ⚠️ Troubleshooting Quick Setup

**If `setup_db.py` fails with connection error:**

1. **Check your internet connection** - Supabase requires internet access
2. **Verify `.env` file exists** - Should be in the project root
3. **Check Supabase project status** - Visit https://supabase.com/dashboard
4. **Firewall issues** - Ensure Python can access external databases

**If table already exists:**
- The script will drop and recreate the table automatically
- Your existing data will be lost (by design for clean setup)

**Still having issues?**
See the [detailed Database Setup](#database-setup) section below.

---

## Table of Contents
- [Quick Setup](#-quick-setup-start-here)
- [Deployment](#-deployment) ⭐ NEW!
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Configuration](#configuration)
- [Running the API](#running-the-api)
- [API Endpoints](#api-endpoints)
- [Testing the API](#testing-the-api)
- [Error Handling](#error-handling)
- [Contributing](#contributing)

---

## 🌐 Deployment

**Share your FNCS application with teammates via public URLs!**

This project is configured for easy deployment:
- **Backend:** Exposed via Ngrok tunnel (local server with public HTTPS URL)
- **Frontend:** Deployed to Vercel (permanent, free hosting)
- **Database:** Already on Supabase (cloud PostgreSQL)

### Quick Deployment Steps:

1. **Start backend locally:**
   ```bash
   python app.py
   ```

2. **Expose backend with Ngrok:**
   ```bash
   python ngrok_setup.py
   ```
   Copy the public URL (e.g., `https://abc123.ngrok-free.app`)

3. **Update frontend environment:**
   Edit `frontend/.env.production` and set:
   ```env
   VITE_API_URL=https://your-ngrok-url.ngrok-free.app
   ```

4. **Deploy frontend to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Import GitHub repository
   - Set Root Directory: `frontend`
   - Add environment variable: `VITE_API_URL`
   - Deploy!

5. **Share the Vercel URL with teammates**

### 📚 Complete Documentation:

For detailed step-by-step instructions, troubleshooting, and advanced configuration, see:
**[DEPLOYMENT.md](./DEPLOYMENT.md)**

The deployment guide includes:
- Complete deployment architecture diagram
- Detailed instructions for each step
- Environment configuration
- Testing checklist
- Troubleshooting guide
- Security best practices
- Maintenance workflow

### Deployment Features:

✅ **Free tier deployment** - $0/month
✅ **HTTPS enabled** - Secure by default
✅ **CORS configured** - Supports ngrok and Vercel domains
✅ **JWT authentication** - Protected API endpoints
✅ **Auto-deployment** - Vercel deploys on git push
✅ **Easy sharing** - Single URL for teammates

---

## Features

- **Complete CRUD Operations**: Create, Read, Update, and Delete categories
- **Data Validation**: Robust input validation for all endpoints
- **Error Handling**: Comprehensive error handling with appropriate HTTP status codes
- **PostgreSQL Integration**: Uses Supabase PostgreSQL database
- **Auto-timestamps**: Automatic `created_at` and `updated_at` management
- **JSON Responses**: All endpoints return JSON formatted responses
- **API Consumer Script**: Ready-to-use script to test all endpoints

---

## Tech Stack

- **Python 3.8+**
- **Flask 3.0.0** - Web framework
- **PostgreSQL** - Database (via Supabase)
- **psycopg2** - PostgreSQL adapter
- **python-dotenv** - Environment variables management
- **requests** - HTTP library for API consumption

---

## Project Structure

```
fncs-crud-categories/
├── .env                  # Environment variables (configured with Supabase credentials)
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── requirements.txt      # Python dependencies
├── app.py                # Flask REST API application
├── consumir.py           # API consumer/testing script
├── setup_db.py           # Database setup and initialization script
├── create_table.sql      # SQL schema for categories table
└── README.md             # Project documentation (this file)
```

---

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- PostgreSQL database (Supabase account recommended)
- Git (optional)

---

## Installation

### 1. Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd fncs-crud-categories

# Or download and extract the ZIP file
```

### 2. Create a Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Database Setup

### 1. Create Supabase Account

1. Go to [https://supabase.com](https://supabase.com)
2. Sign up or log in
3. Create a new project

### 2. Create the Categories Table

In your Supabase SQL Editor, run the following SQL:

```sql
-- Create categories table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create index on name for faster lookups
CREATE INDEX idx_categories_name ON categories(name);

-- Create index on is_active for filtering
CREATE INDEX idx_categories_is_active ON categories(is_active);

-- Create trigger to auto-update updated_at field
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_categories_updated_at
    BEFORE UPDATE ON categories
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

### 3. Get Your Database Connection String

1. In Supabase, go to **Project Settings** → **Database**
2. Find the **Connection String** section
3. Select **URI** format
4. Copy the connection string (it looks like this):
   ```
   postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:5432/postgres
   ```

---

## Configuration

### 1. Create Environment File

Copy the example environment file:

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

### 2. Configure Database Connection

Edit the `.env` file and add your Supabase connection string:

```env
DATABASE_URL=postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:5432/postgres
```

**Important:** Replace the placeholders with your actual Supabase credentials.

---

## Running the API

### 1. Start the Flask Server

```bash
python app.py
```

You should see:

```
============================================================
FNCS Categories API - Starting server
============================================================
Server running on: http://localhost:5000
Database connected: aws-0-us-east-1.pooler.supabase.com:5432/postgres

Available endpoints:
  GET    /categories          - Get all categories
  GET    /categories/<id>     - Get category by ID
  POST   /categories          - Create new category
  PUT    /categories/<id>     - Update category
  DELETE /categories/<id>     - Delete category
============================================================
```

### 2. Verify Server is Running

Open your browser and navigate to:
```
http://localhost:5000/categories
```

You should see a JSON response with an empty categories array.

---

## API Endpoints

### Base URL
```
http://localhost:5000
```

### 1. Get All Categories

**Endpoint:** `GET /categories`

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Technology",
      "description": "Tech news and updates",
      "is_active": true,
      "created_at": "2024-01-15T10:30:00",
      "updated_at": "2024-01-15T10:30:00"
    }
  ],
  "count": 1
}
```

**cURL Example:**
```bash
curl http://localhost:5000/categories
```

---

### 2. Get Category by ID

**Endpoint:** `GET /categories/<id>`

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Technology",
    "description": "Tech news and updates",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
}
```

**cURL Example:**
```bash
curl http://localhost:5000/categories/1
```

---

### 3. Create New Category

**Endpoint:** `POST /categories`

**Request Body:**
```json
{
  "name": "Technology",
  "description": "Tech news and updates",
  "is_active": true
}
```

**Fields:**
- `name` (required): Category name, max 100 characters, must be unique
- `description` (optional): Category description
- `is_active` (optional): Boolean, defaults to `true`

**Response:**
```json
{
  "success": true,
  "message": "Category created successfully",
  "data": {
    "id": 1,
    "name": "Technology",
    "description": "Tech news and updates",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/categories \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Technology\",\"description\":\"Tech news\",\"is_active\":true}"
```

---

### 4. Update Category

**Endpoint:** `PUT /categories/<id>`

**Request Body:**
```json
{
  "name": "Tech & Innovation",
  "description": "Updated description",
  "is_active": false
}
```

**Fields:** (all optional)
- `name`: New category name
- `description`: New description
- `is_active`: New active status

**Note:** The `updated_at` field is automatically updated.

**Response:**
```json
{
  "success": true,
  "message": "Category updated successfully",
  "data": {
    "id": 1,
    "name": "Tech & Innovation",
    "description": "Updated description",
    "is_active": false,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:35:00"
  }
}
```

**cURL Example:**
```bash
curl -X PUT http://localhost:5000/categories/1 \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Tech & Innovation\",\"is_active\":false}"
```

---

### 5. Delete Category

**Endpoint:** `DELETE /categories/<id>`

**Response:**
```json
{
  "success": true,
  "message": "Category \"Technology\" deleted successfully"
}
```

**cURL Example:**
```bash
curl -X DELETE http://localhost:5000/categories/1
```

---

## Testing the API

### Option 1: Using the Consumer Script (Recommended)

The project includes `consumir.py`, a comprehensive script to test all endpoints.

#### Run Full Demo:
```bash
python consumir.py
```

Select option **2** to run a full automated demo that:
- Creates sample categories
- Retrieves them by ID and as a list
- Updates categories
- Deletes categories
- Tests error cases

#### Interactive Menu:
```bash
python consumir.py
```

Select option **1** for an interactive menu where you can:
- Manually test each endpoint
- Create custom categories
- Update specific fields
- View formatted responses

### Option 2: Using cURL

See the cURL examples in the [API Endpoints](#api-endpoints) section above.

### Option 3: Using Postman or Thunder Client

1. Import the endpoints as a collection
2. Set the base URL to `http://localhost:5000`
3. Test each endpoint with different payloads

---

## Error Handling

The API returns appropriate HTTP status codes and error messages:

### Status Codes

- `200 OK` - Successful GET, PUT, DELETE
- `201 Created` - Successful POST
- `400 Bad Request` - Validation error or bad input
- `404 Not Found` - Resource not found
- `405 Method Not Allowed` - Invalid HTTP method
- `500 Internal Server Error` - Server error

### Error Response Format

```json
{
  "success": false,
  "error": "Error message describing what went wrong"
}
```

### Common Errors

**1. Missing Required Field:**
```json
{
  "success": false,
  "error": "Field 'name' is required"
}
```

**2. Duplicate Category Name:**
```json
{
  "success": false,
  "error": "A category with this name already exists"
}
```

**3. Category Not Found:**
```json
{
  "success": false,
  "error": "Category with id 999 not found"
}
```

**4. Invalid Data Type:**
```json
{
  "success": false,
  "error": "Field 'is_active' must be a boolean"
}
```

---

## API Usage Examples

### Example 1: Create Multiple Categories

```python
import requests

categories = [
    {"name": "Technology", "description": "Tech news"},
    {"name": "Finance", "description": "Financial markets"},
    {"name": "Sports", "description": "Sports updates"}
]

for cat in categories:
    response = requests.post(
        "http://localhost:5000/categories",
        json=cat
    )
    print(response.json())
```

### Example 2: Get and Filter Active Categories

```python
import requests

# Get all categories
response = requests.get("http://localhost:5000/categories")
data = response.json()

# Filter active categories in your application
active_categories = [
    cat for cat in data['data']
    if cat['is_active']
]

print(f"Active categories: {len(active_categories)}")
```

### Example 3: Batch Update Categories

```python
import requests

# Deactivate multiple categories
category_ids = [1, 2, 3]

for cat_id in category_ids:
    response = requests.put(
        f"http://localhost:5000/categories/{cat_id}",
        json={"is_active": False}
    )
    print(f"Category {cat_id}: {response.json()['message']}")
```

---

## Development Tips

### Enable Debug Mode

Debug mode is enabled by default in `app.py`. To disable it for production:

```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

### View Database Logs

In Supabase:
1. Go to **Database** → **Roles**
2. Enable **Connection Pooler** logging
3. View logs in **Logs** section

### Test Database Connection

```python
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
print("Connection successful!")
conn.close()
```

---

## Troubleshooting

### Issue: "DATABASE_URL environment variable is not set"

**Solution:** Make sure you created the `.env` file and added your database URL.

### Issue: "Connection refused" when starting the API

**Solution:**
- Check if port 5000 is already in use
- Change the port in `app.py` if needed
- Check your firewall settings

### Issue: "Category with this name already exists"

**Solution:** Category names must be unique. Choose a different name or update the existing category.

### Issue: "Database connection failed"

**Solution:**
- Verify your Supabase credentials in `.env`
- Check if your Supabase project is active
- Ensure your IP is allowed in Supabase settings

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

This project is part of the Financial News Classification System (FNCS).

---

## Contact

For questions or support, please open an issue in the repository.

---

## Acknowledgments

- Flask documentation: https://flask.palletsprojects.com/
- Supabase documentation: https://supabase.com/docs
- PostgreSQL documentation: https://www.postgresql.org/docs/

---

**Happy Coding!** 🚀
