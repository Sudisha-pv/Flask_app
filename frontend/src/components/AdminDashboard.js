import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { feedbackAPI, adminAPI, authAPI } from '../api/api';
import './AdminDashboard.css';

function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [feedback, setFeedback] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
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

      <div className="feedback-section">
        <h2>User Feedback / Sentiment Analysis</h2>
        {loading ? (
          <div className="loading">Loading feedback...</div>
        ) : feedback.length === 0 ? (
          <p>No feedback found</p>
        ) : (
          <div className="feedback-table-container">
            <table className="feedback-table">
              <thead>
                <tr>
                  <th>USER</th>
                  <th>FEEDBACK</th>
                  <th>RATING</th>
                  <th>SENTIMENT</th>
                </tr>
              </thead>
              <tbody>
                {feedback.map((item) => (
                  <tr key={item.id}>
                    <td className="user-cell">{item.username}</td>
                    <td className="feedback-cell">{item.comment}</td>
                    <td className="rating-cell">{item.rating}</td>
                    <td className="sentiment-cell">
                      <span className={`sentiment-badge ${item.sentiment || 'unknown'}`}>
                        {item.sentiment || 'N/A'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default AdminDashboard;
