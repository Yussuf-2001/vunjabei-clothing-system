import React, { useState } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';

const Login = ({ setUser }) => {
  const [formData, setFormData] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError('');
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');
    axios.post('http://127.0.0.1:8000/api/login/', formData)
      .then(res => {
        if (res.data.success) {
          const userData = res.data;
          setUser(userData);
          localStorage.setItem('user', JSON.stringify(userData));
          navigate('/products');
        }
      })
      .catch(err => {
        console.error("Login Error:", err);
        setError("Incorrect username or password");
      });
  };

  return (
    <div className="col-md-6 offset-md-3 mt-5">
      <div className="card shadow">
        <div className="card-header bg-primary text-white">Login - Vunjabei Customer</div>
        <div className="card-body">
          {error && <div className="alert alert-danger text-center">{error}</div>}
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label>Username</label>
              <input type="text" name="username" className="form-control" onChange={handleChange} required />
            </div>
            <div className="mb-3">
              <label>Password</label>
              <input type="password" name="password" className="form-control" onChange={handleChange} required />
            </div>
            <button type="submit" className="btn btn-primary w-100">Login</button>
          </form>
          <p className="mt-3 text-center">
            Don't have an account? <Link to="/register" className="btn btn-link">Register Here</Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;