import React from 'react';
import { Routes, Route, NavLink, Navigate } from 'react-router-dom';
import ProductListPage from './ProductListPage';
import ProductDetailPage from './ProductDetailPage';
import MyOrdersPage from './MyOrdersPage';

const CustomerDashboard = ({ user }) => {
  return (
    <div className="row g-4">
      <div className="col-lg-3">
        <div className="card shadow-sm">
          <div className="card-body">
            <h5 className="card-title">Customer Menu</h5>
            <div className="nav flex-column nav-pills gap-2 mt-3">
              <NavLink
                to="/customer/products"
                className={({ isActive }) => `nav-link ${isActive ? 'active' : 'text-dark'}`}
              >
              Products
              </NavLink>
              <NavLink
                to="/customer/my-orders"
                className={({ isActive }) => `nav-link ${isActive ? 'active' : 'text-dark'}`}
              >
              My Orders
              </NavLink>
            </div>
          </div>
        </div>
      </div>
      <div className="col-lg-9">
        <Routes>
          <Route index element={<Navigate to="products" replace />} />
          <Route path="products" element={<ProductListPage />} />
          <Route path="products/:productId" element={<ProductDetailPage user={user} />} />
          <Route path="my-orders" element={<MyOrdersPage user={user} />} />
          <Route path="*" element={<Navigate to="products" replace />} />
        </Routes>
      </div>
    </div>
  );
};

export default CustomerDashboard;
