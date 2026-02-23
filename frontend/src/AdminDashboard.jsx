import React from 'react';
import { Routes, Route, Link, useLocation, Navigate } from 'react-router-dom';
import DashboardStats from './DashboardStats';
import ProductManagement from './ProductManagement';
import OrderManagement from './OrderManagement';

const AdminDashboard = () => {
  const location = useLocation();

  const isActive = (path) => {
    if (path === '/admin') {
      return location.pathname === '/admin';
    }
    return location.pathname.startsWith(path);
  };

  return (
    <div className="d-flex" style={{ minHeight: '100vh' }}>
      <div className="bg-dark text-white p-3 d-flex flex-column" style={{ width: '260px', minHeight: '100vh', position: 'fixed' }}>
        <h4 className="mb-4 text-danger fw-bold text-center py-2 border-bottom border-secondary">Vunjabei Admin</h4>
        <ul className="nav flex-column gap-2">
          <li className="nav-item">
            <Link to="/admin" className={`nav-link text-white ${isActive('/admin') ? 'bg-danger rounded' : ''}`}>
              Dashboard
            </Link>
          </li>
          <li className="nav-item">
            <Link
              to="/admin/products"
              className={`nav-link text-white ${isActive('/admin/products') ? 'bg-danger rounded' : ''}`}
            >
              Products
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/admin/orders" className={`nav-link text-white ${isActive('/admin/orders') ? 'bg-danger rounded' : ''}`}>
              Orders
            </Link>
          </li>
        </ul>
      </div>

      <div className="flex-grow-1 bg-light" style={{ marginLeft: '260px' }}>
        <Routes>
          <Route index element={<DashboardStats />} />
          <Route path="products" element={<ProductManagement />} />
          <Route path="orders" element={<OrderManagement />} />
          <Route path="*" element={<Navigate to="/admin" replace />} />
        </Routes>
      </div>
    </div>
  );
};

export default AdminDashboard;
