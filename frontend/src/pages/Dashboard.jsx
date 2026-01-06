/**
 * Dashboard Page
 * Main page showing portfolio with stocks list and CRUD operations
 * Protected route - requires authentication
 */

import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import {
  getStocks,
  addStock,
  updateStock,
  deleteStock,
  getPortfolioSummary,
} from '../services/api';

const Dashboard = () => {
  const { user, logout } = useAuth();

  // State for stocks list
  const [stocks, setStocks] = useState([]);
  const [summary, setSummary] = useState(null);

  // State for add/edit form
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingStock, setEditingStock] = useState(null);
  const [formData, setFormData] = useState({
    stock_name: '',
    quantity: '',
    buy_price: '',
  });

  // UI state
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  /**
   * Load stocks and summary when component mounts
   */
  useEffect(() => {
    loadData();
  }, []);

  /**
   * Load stocks and portfolio summary from API
   */
  const loadData = async () => {
    try {
      setLoading(true);
      setError('');

      // Fetch stocks and summary in parallel
      const [stocksData, summaryData] = await Promise.all([
        getStocks(),
        getPortfolioSummary(),
      ]);

      setStocks(stocksData);
      setSummary(summaryData);
    } catch (err) {
      setError('Failed to load portfolio data. Please try again.');
      console.error('Error loading data:', err);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Handle input changes in form
   */
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  /**
   * Handle form submission (add or edit)
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      const stockData = {
        stock_name: formData.stock_name,
        quantity: parseFloat(formData.quantity),
        buy_price: parseFloat(formData.buy_price),
      };

      if (editingStock) {
        // Update existing stock
        await updateStock(editingStock.id, stockData);
        setSuccess('Stock updated successfully!');
      } else {
        // Add new stock
        await addStock(stockData);
        setSuccess('Stock added successfully!');
      }

      // Reset form and reload data
      resetForm();
      await loadData();
    } catch (err) {
      if (err.response && err.response.data && err.response.data.detail) {
        setError(err.response.data.detail);
      } else {
        setError('Operation failed. Please try again.');
      }
    }
  };

  /**
   * Handle delete stock
   */
  const handleDelete = async (stockId) => {
    if (!window.confirm('Are you sure you want to delete this stock?')) {
      return;
    }

    try {
      await deleteStock(stockId);
      setSuccess('Stock deleted successfully!');
      await loadData();
    } catch (err) {
      setError('Failed to delete stock. Please try again.');
    }
  };

  /**
   * Open edit form with stock data
   */
  const handleEdit = (stock) => {
    setEditingStock(stock);
    setFormData({
      stock_name: stock.stock_name,
      quantity: stock.quantity.toString(),
      buy_price: stock.buy_price.toString(),
    });
    setShowAddForm(true);
  };

  /**
   * Reset form to initial state
   */
  const resetForm = () => {
    setFormData({
      stock_name: '',
      quantity: '',
      buy_price: '',
    });
    setEditingStock(null);
    setShowAddForm(false);
    setError('');
    setSuccess('');
  };

  /**
   * Format currency
   */
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(value);
  };

  /**
   * Format percentage
   */
  const formatPercentage = (value) => {
    return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`;
  };

  if (loading && stocks.length === 0) {
    return <div className="loading">Loading portfolio...</div>;
  }

  return (
    <div className="container">
      {/* Header */}
      <div className="header">
        <h1>Stock Portfolio Tracker</h1>
        <div className="header-actions">
          <span style={{ marginRight: '15px' }}>Welcome, {user?.username}!</span>
          <button className="btn btn-secondary btn-small" onClick={logout}>
            Logout
          </button>
        </div>
      </div>

      {/* Portfolio Summary */}
      {summary && (
        <div className="summary-card">
          <h2>Portfolio Summary</h2>
          <div className="summary-stats">
            <div className="stat-item">
              <div className="stat-label">Total Stocks</div>
              <div className="stat-value">{summary.total_stocks}</div>
            </div>
            <div className="stat-item">
              <div className="stat-label">Total Invested</div>
              <div className="stat-value">{formatCurrency(summary.total_invested)}</div>
            </div>
            <div className="stat-item">
              <div className="stat-label">Current Value</div>
              <div className="stat-value">{formatCurrency(summary.total_current_value)}</div>
            </div>
            <div className="stat-item">
              <div className="stat-label">Profit/Loss</div>
              <div
                className={`stat-value ${
                  summary.total_profit_loss >= 0 ? 'positive' : 'negative'
                }`}
              >
                {formatCurrency(summary.total_profit_loss)} (
                {formatPercentage(summary.total_profit_loss_percentage)})
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Messages */}
      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}

      {/* Add Stock Button */}
      {!showAddForm && (
        <button
          className="btn btn-primary"
          onClick={() => setShowAddForm(true)}
          style={{ marginBottom: '20px' }}
        >
          + Add Stock
        </button>
      )}

      {/* Add/Edit Form */}
      {showAddForm && (
        <div className="form-container" style={{ maxWidth: '500px', margin: '20px auto' }}>
          <h2>{editingStock ? 'Edit Stock' : 'Add Stock'}</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="stock_name">Stock Name</label>
              <input
                type="text"
                id="stock_name"
                name="stock_name"
                value={formData.stock_name}
                onChange={handleChange}
                required
                placeholder="e.g., AAPL, GOOGL"
              />
            </div>

            <div className="form-group">
              <label htmlFor="quantity">Quantity</label>
              <input
                type="number"
                id="quantity"
                name="quantity"
                value={formData.quantity}
                onChange={handleChange}
                required
                min="0.01"
                step="0.01"
                placeholder="Number of shares"
              />
            </div>

            <div className="form-group">
              <label htmlFor="buy_price">Buy Price (per share)</label>
              <input
                type="number"
                id="buy_price"
                name="buy_price"
                value={formData.buy_price}
                onChange={handleChange}
                required
                min="0.01"
                step="0.01"
                placeholder="Price per share"
              />
            </div>

            <div style={{ display: 'flex', gap: '10px' }}>
              <button type="submit" className="btn btn-primary" style={{ flex: 1 }}>
                {editingStock ? 'Update' : 'Add'} Stock
              </button>
              <button
                type="button"
                className="btn btn-secondary"
                onClick={resetForm}
                style={{ flex: 1 }}
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Stocks Table */}
      <div className="table-container">
        <h2 style={{ padding: '15px', margin: 0 }}>Your Stocks</h2>
        {stocks.length === 0 ? (
          <div style={{ padding: '40px', textAlign: 'center', color: '#666' }}>
            No stocks in your portfolio. Add your first stock above!
          </div>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Stock Name</th>
                <th>Quantity</th>
                <th>Buy Price</th>
                <th>Current Price</th>
                <th>Total Invested</th>
                <th>Current Value</th>
                <th>Profit/Loss</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {stocks.map((stock) => (
                <tr key={stock.id}>
                  <td>{stock.stock_name}</td>
                  <td>{stock.quantity}</td>
                  <td>{formatCurrency(stock.buy_price)}</td>
                  <td>{formatCurrency(stock.current_price)}</td>
                  <td>{formatCurrency(stock.total_invested)}</td>
                  <td>{formatCurrency(stock.current_value)}</td>
                  <td
                    style={{
                      color: stock.profit_loss >= 0 ? '#4CAF50' : '#f44336',
                      fontWeight: '500',
                    }}
                  >
                    {formatCurrency(stock.profit_loss)} (
                    {formatPercentage(stock.profit_loss_percentage)})
                  </td>
                  <td>
                    <div style={{ display: 'flex', gap: '5px' }}>
                      <button
                        className="btn btn-secondary btn-small"
                        onClick={() => handleEdit(stock)}
                      >
                        Edit
                      </button>
                      <button
                        className="btn btn-danger btn-small"
                        onClick={() => handleDelete(stock.id)}
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default Dashboard;










