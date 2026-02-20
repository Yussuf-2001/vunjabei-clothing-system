import React, { useState } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';

const Register = () => {
  const [formData, setFormData] = useState({ username: '', password: '', email: '' });
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post('http://127.0.0.1:8000/api/register/', formData)
      .then(res => {
        alert("Usajili umefanikiwa! Sasa unaweza ku-login.");
        navigate('/login');
      })
      .catch(err => {
        let errorMessage = "Usajili umeshindikana. Tafadhali jaribu tena.";
        if (err.response && err.response.data) {
            // Tunatoa ujumbe wa kosa kutoka Django na kuuonyesha
            const errors = Object.entries(err.response.data).map(([key, value]) => `${key}: ${value.join(', ')}`);
            errorMessage = errors.join('\n');
        }
        alert(errorMessage);
      });
  };

  return (
    <div className="col-md-6 offset-md-3 mt-5">
      <div className="card shadow">
        <div className="card-header bg-dark text-white">Register - Vunjabei Customer</div>
        <div className="card-body">
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label>Username</label>
              <input type="text" name="username" className="form-control" onChange={handleChange} required />
            </div>
            <div className="mb-3">
              <label>Email (Optional)</label>
              <input type="email" name="email" className="form-control" onChange={handleChange} />
            </div>
            <div className="mb-3">
              <label>Password</label>
              <input type="password" name="password" className="form-control" onChange={handleChange} required />
            </div>
            <button type="submit" className="btn btn-dark w-100">Register</button>
          </form>
          <p className="mt-3 text-center">
            Una akaunti? <Link to="/login" className="btn btn-link">Login Hapa</Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register;