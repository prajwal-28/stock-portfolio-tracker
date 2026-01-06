# MongoDB Atlas Connection Setup

## The SSL Error You're Seeing

If you see an SSL handshake error, it usually means:
1. You're using `mongodb://` instead of `mongodb+srv://` for Atlas
2. Your IP address is not whitelisted
3. Username/password is incorrect

## How to Fix

### Step 1: Get Your Connection String from MongoDB Atlas

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Click "Connect" on your cluster
3. Choose "Connect your application"
4. Copy the connection string

**IMPORTANT:** The connection string should look like:
```
mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

**NOT:**
```
mongodb://...  ❌ (This won't work for Atlas)
```

### Step 2: Replace Placeholders

Replace `<username>` and `<password>` with your actual credentials:
```
mongodb+srv://myuser:mypassword@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

### Step 3: Set Environment Variable

**Windows PowerShell:**
```powershell
$env:MONGODB_URL="mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"
```

**Windows CMD:**
```cmd
set MONGODB_URL=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

**macOS/Linux:**
```bash
export MONGODB_URL="mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"
```

### Step 4: Whitelist Your IP Address

1. In MongoDB Atlas, go to "Network Access"
2. Click "Add IP Address"
3. Click "Add Current IP Address" or enter your IP
4. Click "Confirm"

### Step 5: Verify Database User

1. In MongoDB Atlas, go to "Database Access"
2. Make sure your database user exists
3. Make sure the password is correct

## Alternative: Use .env File

Create a `.env` file in the `backend` directory:

```env
MONGODB_URL=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=stock_portfolio_db
SECRET_KEY=your-secret-key-here
```

The app will automatically load this file.

## Test Your Connection

After setting the environment variable, restart your server:

```bash
uvicorn app.main:app --reload --port 8000
```

You should see:
```
✅ Successfully connected to MongoDB database: stock_portfolio_db
```

## Still Having Issues?

1. **Double-check the connection string format** - Must start with `mongodb+srv://`
2. **Verify IP whitelist** - Your current IP must be allowed
3. **Check username/password** - Make sure they're correct (no special characters need URL encoding)
4. **Try from MongoDB Atlas shell** - Test the connection string in Atlas web shell first











