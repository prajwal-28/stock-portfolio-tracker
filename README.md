# Stock Portfolio Tracker - Full stack application

A full-stack stock portfolio tracking application with a FastAPI backend. This backend provides RESTful APIs for user authentication and portfolio management, featuring dynamic profit/loss calculations using simulated stock prices.

# Project Overview

The Stock Portfolio Tracker is a full-stack web application that allows users to:
- Register and authenticate securely using JWT tokens
- Add stocks to their personal portfolio
- Track investments with real-time profit/loss calculations
- View portfolio summaries with aggregated metrics

**Key Architecture Decision**: Current stock prices are **simulated dynamically** at request time (not stored in the database). This demonstrates backend business logic separation and allows the application to function without external API dependencies. The simulation generates realistic price fluctuations within ±5% of the purchase price.

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework for building APIs
- **MongoDB Atlas** - Cloud-hosted NoSQL database
- **Motor** - Async MongoDB driver for Python
- **JWT (python-jose)** - JSON Web Token authentication
- **Pydantic** - Data validation and serialization
- **Bcrypt (passlib)** - Password hashing
- **Uvicorn** - ASGI server

### Testing
- **Pytest** - Testing framework
- **HTTPX** - Async HTTP client for API testing
- **Pytest-asyncio** - Async test support

## Architecture Overview

```
Frontend (React) ↔ Backend (FastAPI) ↔ Database (MongoDB Atlas)
```

### Separation of Concerns

- **Frontend**: Handles UI/UX, user interactions, and displays data
- **Backend**: Contains all business logic, data validation, and calculations
- **Database**: Stores user data and portfolio entries (buy_price, quantity, etc.)

### Business Logic Location

All business logic resides in the backend:
- Stock price simulation
- Profit/loss calculations
- Portfolio summary aggregations
- Data validation and sanitization

The frontend is a presentation layer that consumes the backend APIs.

## Price Simulation Logic

### Why Simulation?

This project uses **simulated stock prices** instead of real stock APIs for the following reasons:
- **Educational Focus**: Demonstrates backend architecture and business logic without external dependencies
- **Consistency**: Provides predictable, testable behavior for development and demonstration
- **Cost-Free**: No API keys or subscription fees required
- **Reliability**: No dependency on third-party service availability

### How It Works

The price simulation is implemented in `app/utils/price_simulator.py`:

- **Price Range**: Current prices fluctuate within **±5%** of the purchase price (buy_price)
- **Deterministic**: Prices are calculated using a hash of stock_name + current hour, ensuring:
  - Same stock has the same price within the same hour
  - Prices change hourly to simulate market movement
  - Consistent behavior across requests
- **Dynamic Calculation**: Prices are **recalculated on every GET request** (not stored in database)
- **Rounded Values**: All prices are rounded to 2 decimal places

### Example

If a stock was purchased at $150.00:
- Simulated price range: $142.50 - $157.50 (±5%)
- Price remains constant within the same hour
- Price updates hourly to show market fluctuations

### Future Enhancement

The simulation can be easily replaced with real stock API integration by:
1. Replacing `simulate_stock_price()` calls with API fetch logic
2. No database schema changes required
3. No frontend changes needed

## Features

### Authentication
- User registration with email validation
- Secure login with JWT token generation
- Password hashing using bcrypt
- Token-based authentication for protected routes
- Token expiration (30 days, configurable)

### Portfolio Management
- **Create**: Add stocks with name, quantity, and buy price
- **Read**: View all stocks or individual stock details
- **Update**: Modify stock information (partial updates supported)
- **Delete**: Remove stocks from portfolio
- **Summary**: Get aggregated portfolio metrics

### Dynamic Calculations
- Current stock value (quantity × simulated current price)
- Total invested amount (quantity × buy price)
- Profit/loss amount and percentage
- Portfolio-wide totals and averages

### Data Security
- User-specific data isolation (users can only access their own portfolio)
- Secure password storage (hashed, never plain text)
- JWT token validation on every protected request
- Input validation using Pydantic schemas

### Testing
- Automated API tests using pytest and HTTPX
- Test coverage for authentication flows
- Test coverage for portfolio CRUD operations
- Health check endpoint tests

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── database.py           # MongoDB connection management
│   ├── models.py            # Pydantic schemas for validation
│   ├── auth.py              # JWT utilities and password hashing
│   ├── routes/
│   │   ├── auth.py          # Authentication endpoints
│   │   └── portfolio.py     # Portfolio CRUD endpoints
│   └── utils/
│       └── price_simulator.py  # Stock price simulation logic
├── tests/                   # Automated API tests
│   ├── test_auth.py
│   ├── test_portfolio.py
│   └── test_health.py
├── requirements.txt         # Python dependencies
├── requirements-test.txt    # Testing dependencies
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- MongoDB Atlas account (or local MongoDB instance)
- Virtual environment (recommended)

### Installation

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   
   On Windows:
   ```bash
   venv\Scripts\activate
   ```
   
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Environment Variables & Security

**CRITICAL**: This project requires a `.env` file for secure configuration. The `.env` file is **NOT committed to version control** for security reasons.

1. **Create a `.env` file** in the `backend/` directory:
   ```env
   MONGODB_URL=your_mongodb_connection_string
   SECRET_KEY=your_jwt_secret_key_here
   DATABASE_NAME=stock_portfolio_db
   ```

2. **MongoDB URL Format:**
   - **MongoDB Atlas**: `mongodb+srv://username:password@cluster.mongodb.net/`
   - **Local MongoDB**: `mongodb://localhost:27017`

3. **SECRET_KEY**: Generate a strong, random secret key for JWT token signing. Never share or commit this value.

4. **Security Notes:**
   - The `.env` file is listed in `.gitignore`
   - Never commit sensitive credentials to version control
   - Use different keys for development and production
   - For MongoDB Atlas, ensure your IP is whitelisted

### Running the Server

1. **Ensure MongoDB is accessible:**
   - MongoDB Atlas: Verify connection string and IP whitelist
   - Local MongoDB: Start the MongoDB service

2. **Start the FastAPI server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The `--reload` flag enables auto-reload on code changes (development only).

3. **Access the API:**
   - API Base URL: `http://localhost:8000`
   - Interactive API Docs (Swagger): `http://localhost:8000/docs`
   - Alternative API Docs (ReDoc): `http://localhost:8000/redoc`

## API Endpoints

### Authentication Endpoints

#### Register User
- **URL:** `POST /api/auth/register`
- **Description:** Create a new user account
- **Request Body:**
  ```json
  {
    "username": "john_doe",
    "email": "john@example.com",
    "password": "password123"
  }
  ```
- **Response:** JWT token and user information

#### Login
- **URL:** `POST /api/auth/login`
- **Description:** Authenticate and receive JWT token
- **Request Body:**
  ```json
  {
    "username": "john_doe",
    "password": "password123"
  }
  ```
- **Response:** JWT token and user information

#### Get Current User
- **URL:** `GET /api/auth/me`
- **Description:** Get authenticated user's information
- **Headers:** `Authorization: Bearer <token>`
- **Response:** User data (id, username, email)

### Portfolio Endpoints

All portfolio endpoints require authentication (JWT token in `Authorization` header).

#### Add Stock
- **URL:** `POST /api/portfolio/stocks`
- **Description:** Add a new stock to portfolio
- **Request Body:**
  ```json
  {
    "stock_name": "AAPL",
    "quantity": 10,
    "buy_price": 150.50
  }
  ```
- **Response:** Stock data with calculated metrics

#### Get All Stocks
- **URL:** `GET /api/portfolio/stocks`
- **Description:** Get all stocks in user's portfolio
- **Response:** Array of stock objects with simulated current prices

#### Get Single Stock
- **URL:** `GET /api/portfolio/stocks/{stock_id}`
- **Description:** Get a specific stock by ID
- **Response:** Stock object with simulated current price

#### Update Stock
- **URL:** `PUT /api/portfolio/stocks/{stock_id}`
- **Description:** Update stock information (partial update supported)
- **Request Body:** (all fields optional)
  ```json
  {
    "stock_name": "GOOGL",
    "quantity": 5,
    "buy_price": 2000.00
  }
  ```
- **Response:** Updated stock object

#### Delete Stock
- **URL:** `DELETE /api/portfolio/stocks/{stock_id}`
- **Description:** Remove stock from portfolio
- **Response:** Success message

#### Get Portfolio Summary
- **URL:** `GET /api/portfolio/summary`
- **Description:** Get aggregated portfolio metrics
- **Response:**
  ```json
  {
    "total_stocks": 3,
    "total_invested": 5000.00,
    "total_current_value": 5200.00,
    "total_profit_loss": 200.00,
    "total_profit_loss_percentage": 4.00,
    "stocks": [...]
  }
  ```

## Testing

### Running Automated Tests

1. **Install test dependencies:**
   ```bash
   pip install -r requirements-test.txt
   ```

2. **Ensure backend server is running:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

3. **Run all tests:**
   ```bash
   pytest tests/ -v
   ```

4. **Run specific test file:**
   ```bash
   pytest tests/test_auth.py -v
   pytest tests/test_portfolio.py -v
   ```

### Test Coverage

- Authentication flow (register, login, token validation)
- Portfolio CRUD operations
- Protected route access
- Error handling
- Data validation

## Database Schema

### Users Collection
```javascript
{
  "_id": ObjectId("..."),
  "username": "john_doe",
  "email": "john@example.com",
  "hashed_password": "$2b$12$...",
  "created_at": ISODate("...")
}
```

### Portfolio Collection
```javascript
{
  "_id": ObjectId("..."),
  "user_id": "507f1f77bcf86cd799439011",
  "stock_name": "AAPL",
  "quantity": 10,
  "buy_price": 150.50,
  "created_at": ISODate("..."),
  "updated_at": ISODate("...")
}
```

**Note**: `current_price` is **not stored** in the database. It is calculated dynamically using the price simulator on each GET request.

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `MONGODB_URL` | MongoDB connection string | Yes | `mongodb://localhost:27017` |
| `SECRET_KEY` | JWT secret key | Yes | (must be set) |
| `DATABASE_NAME` | Database name | No | `stock_portfolio_db` |

### Default Settings

- Token expiration: 30 days
- Server port: 8000
- CORS origins: `localhost:3000`, `localhost:5173`

## Troubleshooting

### MongoDB Connection Error
- Verify MongoDB is running (local) or connection string is correct (Atlas)
- Check IP whitelist in MongoDB Atlas
- Ensure `MONGODB_URL` is set correctly in `.env`

### Import Errors
- Activate virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`

### Port Already in Use
- Change port: `uvicorn app.main:app --reload --port 8001`
- Or stop the process using port 8000

### Authentication Errors
- Verify `SECRET_KEY` is set in `.env`
- Check token expiration (default: 30 days)
- Ensure token is included in `Authorization: Bearer <token>` header

## Notes for Recruiters

This project demonstrates:

- **Backend Architecture**: Clean separation of concerns, business logic in backend
- **API Design**: RESTful endpoints with proper HTTP methods and status codes
- **Security**: JWT authentication, password hashing, user data isolation
- **Data Validation**: Pydantic schemas for request/response validation
- **Testing**: Automated API tests with pytest
- **Documentation**: Comprehensive API documentation via Swagger/ReDoc

The price simulation is an **intentional design choice** that:
- Demonstrates backend business logic without external dependencies
- Can be easily replaced with real stock APIs when needed
- Provides consistent, testable behavior for demonstration purposes

The codebase follows best practices for maintainability, security, and scalability.

## Deployment

This project is currently configured to run in a local development environment.
The architecture is deployment-ready and can be hosted on platforms like Render,
Railway, or Vercel if needed.


