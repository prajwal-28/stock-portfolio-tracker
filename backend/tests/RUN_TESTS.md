# Quick Test Run Guide

## 🚀 Fastest Way to Run Tests

### Step 1: Make sure backend is running
```bash
# In one terminal
cd backend
uvicorn app.main:app --reload --port 8000
```

### Step 2: Install test dependencies (one time only)
```bash
cd backend
pip install -r requirements-test.txt
```

### Step 3: Run all tests
```bash
cd backend
pytest tests/ -v
```

## 📋 Test Commands Cheat Sheet

```bash
# Run all tests
pytest tests/

# Run all tests with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_health.py -v
pytest tests/test_auth.py -v
pytest tests/test_portfolio.py -v

# Run specific test function
pytest tests/test_auth.py::test_user_login -v

# Run tests and show print statements
pytest tests/ -v -s

# Run tests and stop on first failure
pytest tests/ -x

# Run tests with coverage (if pytest-cov installed)
pytest tests/ --cov=app
```

## ✅ Expected Output

When everything works:
```
======================== test session starts ========================
collected 20 items

tests/test_health.py::test_root_endpoint PASSED
tests/test_health.py::test_health_endpoint PASSED
tests/test_health.py::test_api_docs_available PASSED
tests/test_auth.py::test_user_registration PASSED
tests/test_auth.py::test_user_login PASSED
... (15 more tests)

======================= 20 passed in 2.34s ========================
```

## ❌ Common Issues

**"Connection refused"**
→ Backend is not running. Start it first!

**"401 Unauthorized"**
→ Check MongoDB connection. Backend needs database.

**"Module not found"**
→ Run: `pip install -r requirements-test.txt`

## 🎯 What Gets Tested

- ✅ Server health and basic endpoints
- ✅ User registration and login
- ✅ JWT token generation and validation
- ✅ Adding stocks to portfolio
- ✅ Viewing all stocks
- ✅ Updating stocks
- ✅ Deleting stocks
- ✅ Portfolio summary calculations
- ✅ Authentication protection
- ✅ Data validation

**Total: 20 automated tests**










