import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { feedbackAPI, adminAPI, authAPI } from '../api/api';
import './AdminDashboard.css';

function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [feedback, setFeedback] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filters, setFilters] = useState({
    sentiment: '',
    rating: '',
    search: ''
  });
  const navigate = useNavigate();

  useEffect(() => {
    const adminToken = localStorage.getItem('adminToken');
    if (!adminToken) {
      navigate('/admin/login');
      return;
    }
    loadDashboardData();
  }, [navigate]);

  const loadDashboardData = async () => {
    const adminToken = localStorage.getItem('adminToken');
    setLoading(true);
    setError('');

    try {
      const [statsResponse, feedbackResponse] = await Promise.all([
        adminAPI.getStats(adminToken),
        feedbackAPI.getAll(adminToken)
      ]);

      if (statsResponse.data.success) {
        setStats(statsResponse.data.stats);
      }
      if (feedbackResponse.data.success) {
        setFeedback(feedbackResponse.data.feedback);
      }
    } catch (err) {
      if (err.response?.status === 403) {
        localStorage.removeItem('adminToken');
        navigate('/admin/login');
      } else {
        setError('Failed to load dashboard data');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = async () => {
    const adminToken = localStorage.getItem('adminToken');
    setLoading(true);

    try {
      const filterParams = {};
      if (filters.sentiment) filterParams.sentiment = filters.sentiment;
      if (filters.rating) filterParams.rating = filters.rating;
      if (filters.search) filterParams.search = filters.search;

      const response = await feedbackAPI.getAll(adminToken, filterParams);
      if (response.data.success) {
        setFeedback(response.data.feedback);
      }
    } catch (err) {
      setError('Failed to filter feedback');
    } finally {
      setLoading(false);
    }
  };

  const clearFilters = () => {
    setFilters({ sentiment: '', rating: '', search: '' });
    loadDashboardData();
  };

  const handleLogout = async () => {
    const adminToken = localStorage.getItem('adminToken');
    try {
      await authAPI.logout(adminToken);
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      localStorage.removeItem('adminToken');
      navigate('/admin/login');
    }
  };

  if (loading && !stats) {
    return <div className="loading">Loading dashboard...</div>;
  }

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Admin Dashboard</h1>
        <button onClick={handleLogout} className="logout-btn">Logout</button>
      </div>

      {error && <div className="error">{error}</div>}

      {stats && (
        <div className="stats-grid">
          <div className="stat-card">
            <h3>Total Users</h3>
            <p className="stat-value">{stats.total_users}</p>
          </div>
          <div className="stat-card">
            <h3>Total Feedback</h3>
            <p className="stat-value">{stats.total_feedback}</p>
          </div>
          <div className="stat-card">
            <h3>Average Rating</h3>
            <p className="stat-value">{stats.average_rating.toFixed(2)}</p>
          </div>
          <div className="stat-card sentiment-card">
            <h3>Sentiment Distribution</h3>
            <div className="sentiment-stats">
              <div className="sentiment-item positive">
                Positive: {stats.sentiment_distribution.positive}
              </div>
              <div className="sentiment-item neutral">
                Neutral: {stats.sentiment_distribution.neutral}
              </div>
              <div className="sentiment-item negative">
                Negative: {stats.sentiment_distribution.negative}
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="filters-section">
        <h2>Filter Feedback</h2>
        <div className="filters-grid">
          <div className="filter-group">
            <label>Search</label>
            <input
              type="text"
              value={filters.search}
              onChange={(e) => setFilters({ ...filters, search: e.target.value })}
              placeholder="Search comments or username..."
            />
          </div>
          <div className="filter-group">
            <label>Sentiment</label>
            <select
              value={filters.sentiment}
              onChange={(e) => setFilters({ ...filters, sentiment: e.target.value })}
            >
              <option value="">All</option>
              <option value="positive">Positive</option>
              <option value="neutral">Neutral</option>
              <option value="negative">Negative</option>
            </select>
          </div>
          <div className="filter-group">
            <label>Rating</label>
            <select
              value={filters.rating}
              onChange={(e) => setFilters({ ...filters, rating: e.target.value })}
            >
              <option value="">All</option>
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
              <option value="5">5</option>
            </select>
          </div>
        </div>
        <div className="filter-buttons">
          <button onClick={handleFilterChange}>Apply Filters</button>
          <button onClick={clearFilters} className="clear-btn">Clear Filters</button>
        </div>
      </div>

      <div className="feedback-section">
        <h2>All Feedback ({feedback.length})</h2>
        {loading ? (
          <div className="loading">Loading feedback...</div>
        ) : feedback.length === 0 ? (
          <p>No feedback found</p>
        ) : (
          <div className="feedback-list">
            {feedback.map((item) => (
              <div key={item.id} className="feedback-card">
                <div className="feedback-header">
                  <span className="username">{item.username}</span>
                  <span className="rating">Rating: {item.rating}/5</span>
                  <span className={`sentiment ${item.sentiment || 'unknown'}`}>
                    {item.sentiment || 'N/A'}
                  </span>
                </div>
                <p className="comment">{item.comment}</p>
                <span className="timestamp">
                  {new Date(item.created_at).toLocaleString()}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default AdminDashboard;
