# 🚀 FNCS Quick Start Guide

## Setup in 3 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Setup Database
```bash
python setup_db.py
```

**What this does:**
- ✅ Tests connection to Supabase
- ✅ Creates categories table
- ✅ Adds 10 sample categories
- ✅ Verifies everything works

### Step 3: Start API
```bash
python app.py
```

**API is now running at:** http://localhost:5000

### Step 4: Test API
```bash
python consumir.py
```

Choose option **2** for full demo or **1** for interactive mode.

---

## Quick Test with cURL

```bash
# Get all categories
curl http://localhost:5000/categories

# Get category by ID
curl http://localhost:5000/categories/1

# Create new category
curl -X POST http://localhost:5000/categories \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Test Category\",\"description\":\"Test description\"}"

# Update category
curl -X PUT http://localhost:5000/categories/1 \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Updated Name\"}"

# Delete category
curl -X DELETE http://localhost:5000/categories/1
```

---

## Project Files

| File | Purpose |
|------|---------|
| `app.py` | Flask REST API server |
| `consumir.py` | Test all endpoints |
| `setup_db.py` | Database initialization |
| `create_table.sql` | Table schema |
| `.env` | Database credentials (already configured) |

---

## Troubleshooting

**Connection Error?**
1. Check internet connection
2. Verify `.env` file exists
3. Visit https://supabase.com/dashboard to check project status

**Port 5000 already in use?**
Edit `app.py` line 441 and change the port number:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Changed to 5001
```

**Table already exists?**
Run `python setup_db.py` again - it will drop and recreate the table.

---

## What's Next?

1. ✅ **Explore the API** - Try all endpoints with `consumir.py`
2. ✅ **Read the docs** - Check `README.md` for detailed documentation
3. ✅ **Customize** - Add your own categories via API
4. ✅ **Integrate** - Use this API in your financial news classification system

---

**Need help?** Check the full README.md for detailed documentation.

**Happy Coding! 🎉**
