import React, { useCallback, useEffect, useState } from 'react';
import api from './api';

const OrderManagement = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  const storedUser = (() => {
    try {
      return JSON.parse(localStorage.getItem('user') || 'null');
    } catch {
      return null;
    }
  })();

  const fetchOrders = useCallback(async () => {
    try {
      const res = await api.get('orders/', { params: { username: storedUser?.username } });
      setOrders(res.data);
    } catch (error) {
      console.error('Error fetching orders:', error);
    } finally {
      setLoading(false);
    }
  }, [storedUser?.username]);

  useEffect(() => {
    fetchOrders();
  }, [fetchOrders]);

  const handleStatusChange = async (orderId, newStatus) => {
    try {
      await api.post(`orders/${orderId}/update-status/`, {
        status: newStatus,
        username: storedUser?.username,
      });
      setOrders((prev) => prev.map((order) => (order.id === orderId ? { ...order, status: newStatus } : order)));
    } catch (error) {
      console.error('Error updating order status:', error);
      alert('Failed to update status');
    }
  };

  if (loading) {
    return <div className="p-4">Loading orders...</div>;
  }

  return (
    <div className="card shadow-sm m-4">
      <div className="card-header bg-white py-3">
        <h5 className="m-0 fw-bold text-secondary">Order Management</h5>
      </div>
      <div className="card-body p-0">
        <div className="table-responsive">
          <table className="table table-striped table-hover mb-0">
            <thead className="bg-light">
              <tr>
                <th>ID</th>
                <th>Customer</th>
                <th>Product</th>
                <th>Quantity</th>
                <th>Total (TSh)</th>
                <th>Date</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {orders.map((order) => (
                <tr key={order.id}>
                  <td>#{order.id}</td>
                  <td>
                    <strong>{order.customer}</strong>
                    <br />
                    <small className="text-muted">{order.phone}</small>
                  </td>
                  <td>{order.product_name}</td>
                  <td>{order.quantity}</td>
                  <td>{parseFloat(order.total_price).toLocaleString()}</td>
                  <td>{order.date}</td>
                  <td>
                    <select
                      className={`form-select form-select-sm ${order.status === 'Pending' ? 'border-warning text-warning' : 'border-success text-success'}`}
                      value={order.status}
                      onChange={(e) => handleStatusChange(order.id, e.target.value)}
                    >
                      <option value="Pending">Pending</option>
                      <option value="Processing">Processing</option>
                      <option value="Shipped">Shipped</option>
                      <option value="Delivered">Delivered</option>
                      <option value="Cancelled">Cancelled</option>
                    </select>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default OrderManagement;
