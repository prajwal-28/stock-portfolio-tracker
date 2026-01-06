# API Tests for Stock Portfolio Tracker

Automated API tests using pytest and httpx to verify backend functionality.

## 📋 Test Coverage

### 1. Health Check Tests (`test_health.py`)
- ✅ Root endpoint (`/`)
- ✅ Health endpoint (`/health`)
- ✅ API documentation (`/docs`)

### 2. Authentication Tests (`test_auth.py`)
- ✅ User registration
- ✅ Duplicate username handling
- ✅ User login
- ✅ Invalid credentials handling
- ✅ JWT token generation
- ✅ Protected route access with token
- ✅ Protected route access without token (should fail)
- ✅ Invalid token handling

### 3. Portfolio Tests (`test_portfolio.py`)
- ✅ Add stock to portfolio
- ✅ Get all stocks
- ✅ Get single stock by ID
- ✅ Update stock (partial update)
- ✅ Delete stock
- ✅ Portfolio summary with totals
- ✅ Unauthorized access (should fail)
- ✅ Invalid data validation

## 🚀 Quick Start

### Prerequisites

1. **Backend must be running** at `http://127.0.0.1:8000`
   ```bash
   cd backend
   uvicorn app.main:app --reload --port 8000
   ```

2. **MongoDB must be running** (local or Atlas)

### Installation

1. **Install test dependencies:**
   ```bash
   cd backend
   pip install -r requirements-test.txt
   ```

   Or install all dependencies at once:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-test.txt
   ```

### Running Tests

#### Run all tests:
```bash
cd backend
pytest tests/
```

#### Run specific test file:
```bash
# Health tests only
pytest tests/test_health.py

# Authentication tests only
pytest tests/test_auth.py

# Portfolio tests only
pytest tests/test_portfolio.py
```

#### Run specific test:
```bash
# Run a single test function
pytest tests/test_auth.py::test_user_login -v
```

#### Run with verbose output:
```bash
pytest tests/ -v
```

#### Run with detailed output:
```bash
pytest tests/ -vv
```

#### Run and show print statements:
```bash
pytest tests/ -v -s
```

## 📊 Expected Test Results

When all tests pass, you should see:

```
======================== test session starts ========================
collected 20 items

tests/test_health.py::test_root_endpoint PASSED
tests/test_health.py::test_health_endpoint PASSED
tests/test_health.py::test_api_docs_available PASSED
tests/test_auth.py::test_user_registration PASSED
tests/test_auth.py::test_user_login PASSED
tests/test_auth.py::test_get_current_user_with_token PASSED
... (more tests)

======================= 20 passed in X.XXs ========================
```

## 🔧 Test Configuration

### Base URL
Tests connect to: `http://127.0.0.1:8000`

To change this, edit `tests/conftest.py`:
```python
BASE_URL = "http://your-backend-url:port"
```

### Test User Credentials
Default test user (defined in `conftest.py`):
- Username: `testuser_api`
- Email: `testuser_api@example.com`
- Password: `testpass123`

The tests automatically register/login this user if needed.

## 🐛 Troubleshooting

### Tests fail with "Connection refused"
- **Problem:** Backend is not running
- **Solution:** Start the backend server:
  ```bash
  uvicorn app.main:app --reload --port 8000
  ```

### Tests fail with "401 Unauthorized"
- **Problem:** JWT token not being generated correctly
- **Solution:** Check that authentication endpoints are working. Test manually:
  ```bash
  curl -X POST http://127.0.0.1:8000/api/auth/register \
    -H "Content-Type: application/json" \
    -d '{"username":"test","email":"test@example.com","password":"test123"}'
  ```

### Tests fail with "Database connection error"
- **Problem:** MongoDB is not running or connection string is wrong
- **Solution:** 
  - Check MongoDB is running
  - Verify `MONGODB_URL` environment variable
  - Check MongoDB Atlas IP whitelist (if using Atlas)

### Import errors
- **Problem:** Missing dependencies
- **Solution:** 
  ```bash
  pip install -r requirements.txt
  pip install -r requirements-test.txt
  ```

### Tests create duplicate users
- **Problem:** Tests are creating users that already exist
- **Solution:** This is handled automatically - tests will login if user exists

## 📝 Test Structure

```
tests/
├── __init__.py           # Package marker
├── conftest.py           # Shared fixtures (client, auth_token, etc.)
├── test_health.py         # Health check tests
├── test_auth.py           # Authentication tests
└── test_portfolio.py      # Portfolio CRUD tests
```

## 🎯 What Each Test Verifies

### Health Tests
- Server is running and responding
- Basic endpoints return expected data
- API documentation is accessible

### Auth Tests
- Users can register with valid data
- Duplicate usernames are rejected
- Users can login with correct credentials
- Wrong passwords are rejected
- JWT tokens are generated and valid
- Protected routes require authentication
- Invalid tokens are rejected

### Portfolio Tests
- Stocks can be added with correct data
- All stocks can be retrieved
- Individual stocks can be retrieved by ID
- Stocks can be updated (partial updates work)
- Stocks can be deleted
- Portfolio summary calculates totals correctly
- Unauthorized access is blocked
- Invalid data is rejected

## 💡 Tips

1. **Run tests before committing code** to ensure nothing broke
2. **Use `-v` flag** to see which tests pass/fail
3. **Use `-s` flag** to see print statements for debugging
4. **Run specific tests** when developing new features
5. **Check test output** for detailed error messages

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [httpx Documentation](https://www.python-httpx.org/)
- [FastAPI Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/)










