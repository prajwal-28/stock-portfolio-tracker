# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
cd frontend
npm install
```

### Step 2: Make Sure Backend is Running
```bash
# In another terminal, start the backend
cd backend
uvicorn app.main:app --reload --port 8000
```

### Step 3: Start Frontend
```bash
# In frontend directory
npm run dev
```

The app will open automatically at `http://localhost:3000`

## ✅ What You'll See

1. **Login Page** - If not logged in
2. **Register** - Create a new account
3. **Dashboard** - View and manage your stock portfolio

## 🎯 First Time Setup

1. Click "Register here" on login page
2. Create an account (username, email, password)
3. You'll be automatically logged in
4. Start adding stocks to your portfolio!

## 📝 Test Credentials

After registering, you can use:
- Username: (your registered username)
- Password: (your registered password)

## 🐛 Common Issues

**"Network Error"**
→ Backend is not running. Start it first!

**"401 Unauthorized"**
→ Token expired. Just login again.

**Port 3000 in use**
→ Change port in `vite.config.js` or stop other app.

## 📚 Next Steps

- Add stocks to your portfolio
- View portfolio summary
- Edit or delete stocks
- Track your profit/loss

Enjoy tracking your stocks! 📈










