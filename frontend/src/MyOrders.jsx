import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const MyOrders = ({ user }) => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user) {
      axios.get(`http://127.0.0.1:8000/api/my-orders/?user_id=${user.id}`)
        .then(res => {
          setOrders(res.data);
          setLoading(false);
        })
        .catch(err => {
          console.error("Error fetching orders:", err);
          setLoading(false);
        });
    }
  }, [user]);

  if (loading) return <div className="text-center mt-5">Loading your orders...</div>;

  return (
    <div className="container mt-4">
      <h2 className="mb-4 fw-bold text-secondary">My Order History</h2>
      
      {orders.length === 0 ? (
        <div className="alert alert-info">
          You haven't placed any orders yet. <Link to="/products">Start Shopping</Link>
        </div>
      ) : (
        <div className="card shadow border-0">
          <div className="card-body p-0">
            <div className="table-responsive">
              <table className="table table-hover mb-0">
                <thead className="bg-light">
                  <tr>
                    <th>Order ID</th>
                    <th>Product</th>
                    <th>Qty</th>
                    <th>Total (TSh)</th>
                    <th>Date</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {orders.map(order => (
                    <tr key={order.id}>
                      <td>#{order.id}</td>
                      <td className="fw-bold">{order.product_name}</td>
                      <td>{order.quantity}</td>
                      <td>{parseFloat(order.total_price).toLocaleString()}</td>
                      <td>{order.date}</td>
                      <td>
                        <span className={`badge ${order.status === 'Pending' ? 'bg-warning text-dark' : order.status === 'Delivered' ? 'bg-success' : 'bg-secondary'}`}>
                          {order.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MyOrders;