# Stock Portfolio Tracker - Frontend

React frontend for the Stock Portfolio Tracker application.

## 📋 Features

- ✅ User registration and login
- ✅ JWT token authentication
- ✅ Protected routes
- ✅ View portfolio with all stocks
- ✅ Add new stocks
- ✅ Edit existing stocks
- ✅ Delete stocks
- ✅ Portfolio summary with totals
- ✅ Profit/loss calculations

## 🚀 Quick Start

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Backend server running at `http://127.0.0.1:8000`

### Installation

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

   Or with yarn:
   ```bash
   yarn install
   ```

### Running the Frontend

1. **Start the development server:**
   ```bash
   npm run dev
   ```

   Or with yarn:
   ```bash
   yarn dev
   ```

2. **Open your browser:**
   - The app will automatically open at `http://localhost:3000`
   - Or manually navigate to `http://localhost:3000`

### Building for Production

```bash
npm run build
```

This creates an optimized production build in the `dist` folder.

## 📁 Project Structure

```
frontend/
├── public/                 # Static files
├── src/
│   ├── components/         # React components
│   │   └── ProtectedRoute.jsx
│   ├── context/            # React context
│   │   └── AuthContext.jsx
│   ├── pages/              # Page components
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   └── Dashboard.jsx
│   ├── services/           # API service layer
│   │   └── api.js
│   ├── App.jsx             # Main app component
│   ├── main.jsx            # Entry point
│   └── index.css           # Global styles
├── index.html
├── package.json
├── vite.config.js
└── README.md
```

## 🔧 Configuration

### Backend URL

The backend URL is configured in `src/services/api.js`:

```javascript
const API_BASE_URL = 'http://127.0.0.1:8000';
```

To change it, edit this file.

### Port

The frontend runs on port 3000 by default. To change it, edit `vite.config.js`:

```javascript
server: {
  port: 3000,  // Change this
}
```

## 🔐 Authentication Flow

1. **Register/Login**: User enters credentials
2. **Token Storage**: JWT token is saved to `localStorage`
3. **Automatic Token Attachment**: Axios interceptor adds token to all API requests
4. **Protected Routes**: Routes check authentication before rendering
5. **Auto Logout**: If token is invalid (401), user is redirected to login

## 📱 Pages

### Login Page (`/login`)
- Username and password form
- Link to register page
- Redirects to dashboard on success

### Register Page (`/register`)
- Username, email, and password form
- Link to login page
- Auto-login after registration

### Dashboard Page (`/dashboard`)
- Portfolio summary (totals, profit/loss)
- List of all stocks in a table
- Add stock form
- Edit stock functionality
- Delete stock with confirmation
- Logout button

## 🛠️ Technologies Used

- **React 18** - UI library
- **React Router DOM** - Routing
- **Axios** - HTTP client
- **Vite** - Build tool and dev server
- **CSS** - Styling (vanilla CSS)

## 📝 API Integration

All API calls are handled in `src/services/api.js`:

- `register()` - User registration
- `login()` - User login
- `getStocks()` - Get all stocks
- `addStock()` - Add new stock
- `updateStock()` - Update stock
- `deleteStock()` - Delete stock
- `getPortfolioSummary()` - Get portfolio totals

## 🐛 Troubleshooting

### "Network Error" or "Connection Refused"
- **Problem**: Backend is not running
- **Solution**: Start the backend server at `http://127.0.0.1:8000`

### "401 Unauthorized" errors
- **Problem**: Token is invalid or expired
- **Solution**: Logout and login again

### Port 3000 already in use
- **Problem**: Another app is using port 3000
- **Solution**: Change port in `vite.config.js` or stop the other app

### Dependencies not installing
- **Problem**: Node.js version too old
- **Solution**: Update Node.js to v16 or higher

## 📚 Development

### Adding New Features

1. **New API endpoint**: Add function to `src/services/api.js`
2. **New page**: Create component in `src/pages/` and add route in `App.jsx`
3. **New component**: Create in `src/components/`

### Code Style

- Use functional components with hooks
- Keep components focused and small
- Add comments explaining complex logic
- Use meaningful variable names

## 🎨 Styling

The app uses vanilla CSS with a simple, clean design:
- Responsive layout
- Clean forms
- Readable tables
- Clear error/success messages

To customize styles, edit `src/index.css`.

## 📄 License

This project is for educational purposes.










