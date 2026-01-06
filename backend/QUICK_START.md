# Quick Start Guide

## Step 1: Install Dependencies

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# or: source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

## Step 2: Start MongoDB

Make sure MongoDB is running on your system:
- **Local MongoDB**: Start MongoDB service**
- **MongoDB Atlas**: Use your connection string

## Step 3: Run the Server

```bash
uvicorn app.main:app --reload --port 8000
```

## Step 4: Test the API

1. Open browser: `http://localhost:8000/docs`
2. Try the `/api/auth/register` endpoint
3. Copy the `access_token` from response
4. Click "Authorize" button (top right)
5. Paste token: `Bearer <your-token>`
6. Test portfolio endpoints

## What You Get

✅ User registration and login
✅ JWT token authentication
✅ Add/View/Update/Delete stocks
✅ Portfolio summary with calculations
✅ Clean JSON responses
✅ Automatic API documentation

## Next: Frontend Development

Once backend is working, we'll build the React frontend!












