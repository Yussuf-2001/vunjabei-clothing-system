import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from './api';

const Login = ({ setUser }) => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await api.post('login/', { username, password });
      const loggedUser = {
        username: response.data.username,
        is_staff: response.data.is_staff,
      };

      localStorage.setItem('user', JSON.stringify(loggedUser));
      setUser(loggedUser);
      navigate(loggedUser.is_staff ? '/admin' : '/customer', { replace: true });
    } catch (requestError) {
      if (!requestError.response) {
        setError('Cannot reach backend API. Ensure backend is running at http://127.0.0.1:8000.');
      } else {
        setError(requestError.response?.data?.error || 'Login failed. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="row justify-content-center">
        <div className="col-md-6 col-lg-4">
          <div className="card shadow-sm">
            <div className="card-body p-4">
              <h3 className="card-title mb-3">Login</h3>
              {error && <div className="alert alert-danger">{error}</div>}
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label className="form-label">Username or Email</label>
                  <input
                    type="text"
                    className="form-control"
                    value={username}
                    onChange={(event) => setUsername(event.target.value)}
                    placeholder="Enter username or email"
                    required
                  />
                  <small className="text-muted">Username/email is not case-sensitive.</small>
                </div>
                <div className="mb-3">
                  <label className="form-label">Password</label>
                  <input
                    type="password"
                    className="form-control"
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                    required
                  />
                  <small className="text-muted">Password is case-sensitive.</small>
                </div>
                <button type="submit" className="btn btn-primary w-100" disabled={loading}>
                  {loading ? 'Logging in...' : 'Login'}
                </button>
              </form>
              <p className="mt-3 mb-0 text-muted">
                New user? <Link to="/register">Create account</Link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
