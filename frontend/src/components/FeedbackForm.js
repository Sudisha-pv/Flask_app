import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { feedbackAPI, authAPI } from '../api/api';

function FeedbackForm() {
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const sessionToken = localStorage.getItem('sessionToken');
    if (!sessionToken) {
      navigate('/login');
    }
  }, [navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    const sessionToken = localStorage.getItem('sessionToken');

    try {
      const response = await feedbackAPI.submit(sessionToken, rating, comment);
      if (response.data.success) {
        setSuccess(`Feedback submitted successfully! Sentiment: ${response.data.sentiment || 'analyzing...'}`);
        setComment('');
        setRating(5);
      } else {
        setError(response.data.message);
      }
    } catch (err) {
      if (err.response?.status === 401) {
        localStorage.removeItem('sessionToken');
        navigate('/login');
      } else {
        setError(err.response?.data?.message || 'Failed to submit feedback');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    const sessionToken = localStorage.getItem('sessionToken');
    try {
      await authAPI.logout(sessionToken);
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      localStorage.removeItem('sessionToken');
      navigate('/login');
    }
  };

  return (
    <div className="container">
      <h1>Submit Feedback</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Rating (1-5)</label>
          <select value={rating} onChange={(e) => setRating(Number(e.target.value))}>
            <option value={1}>1 - Poor</option>
            <option value={2}>2 - Fair</option>
            <option value={3}>3 - Good</option>
            <option value={4}>4 - Very Good</option>
            <option value={5}>5 - Excellent</option>
          </select>
        </div>
        <div className="form-group">
          <label>Comment</label>
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="Share your experience..."
            required
          />
        </div>
        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}
        <button type="submit" disabled={loading}>
          {loading ? 'Submitting...' : 'Submit Feedback'}
        </button>
      </form>
      <div className="link" onClick={handleLogout}>
        Logout
      </div>
    </div>
  );
}

export default FeedbackForm;
