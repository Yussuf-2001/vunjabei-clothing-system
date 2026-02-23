import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

import AdminDashboard from './AdminDashboard';
import CustomerDashboard from './CustomerDashboard';
import Navbar from './components/Navbar.jsx';
import RoleRoute from './components/RoleRoute';
import Login from './Login';
import Register from './Register';

function App() {
  const [user, setUser] = useState(() => {
    const storedUser = localStorage.getItem('user');
    if (!storedUser) {
      return null;
    }

    try {
      return JSON.parse(storedUser);
    } catch (error) {
      console.error('Invalid user in localStorage', error);
      localStorage.removeItem('user');
      return null;
    }
  });

  const defaultRoute = user ? (user.is_staff ? '/admin' : '/customer') : '/login';

  return (
    <Router>
      <Navbar user={user} setUser={setUser} />
      <div className="mt-4">
        <Routes>
          <Route path="/" element={<Navigate to={defaultRoute} replace />} />
          <Route path="/login" element={user ? <Navigate to={defaultRoute} replace /> : <Login setUser={setUser} />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/admin/*"
            element={
              <RoleRoute user={user} requiredRole="admin">
                <AdminDashboard />
              </RoleRoute>
            }
          />
          <Route
            path="/customer/*"
            element={
              <RoleRoute user={user} requiredRole="customer">
                <CustomerDashboard user={user} />
              </RoleRoute>
            }
          />
          <Route path="*" element={<Navigate to={defaultRoute} replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
