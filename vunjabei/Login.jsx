import React, { useState } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';

const Login = ({ setUser }) => {
  const [formData, setFormData] = useState({ username: '', password: '' });
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
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
        alert("Login imeshindikana. Hakiki jina na password yako.");
      });
  };

  return (
    <div className="col-md-6 offset-md-3 mt-5">
      <div className="card shadow">
        <div className="card-header bg-primary text-white">Login - Vunjabei Customer</div>
        <div className="card-body">
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
            Huna akaunti? <Link to="/register" className="btn btn-link">Jisajili Hapa</Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;